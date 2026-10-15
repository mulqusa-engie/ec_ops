# analytics_rec.py
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import pandas as pd
import pyodbc


@dataclass
class DbConfig:
    """Holds connection strings for MSSQL and Oracle (Zainet)."""
    mssql_conn_str: str
    oracle_conn_str: Optional[str] = None  # optional; not used by default


class RecOpsData:
    """
    Loads REC P&L and Position data from SQL Server, applies mappings,
    and builds summary calc objects (pos_dict, pos_nd, pivots) on init.

    Attributes after init:
        pos_df: Raw position dataframe (SQL result merged with mapping)
        pnl_df: Raw pnl dataframe (SQL result)
        mapping_df: Curve mapping dataframe
        pos_dict: dict[str, pd.DataFrame] — summary pivot tables for DELTA
        pos_nd:   dict[str, pd.DataFrame] — summary pivot tables for DELTA_ND
        rec_pnl_pivot: P&L pivot (BOOK x YEAR) with totals
        pjm_pos_disc: Discounted PJM pivot (index=['TYPE','MAPPING'], cols=YEAR)
        pjm_pos_nd:   Non-discounted PJM pivot
        pos_level_pnl: Optional detailed P&L (if as_of_date and query provided)
    """

    def __init__(
        self,
        run_on_init: bool = False,        
        pnl_sql_path: str = "",
        pos_sql_path: str = "",
        mapping_path: str = "",
        db: DbConfig = DbConfig(""),
        mapping_sheet: str = "ALIGNE",
        vol_books: Optional[list[str]] = None,
        northeast_books: Optional[list[str]] = None,
        as_of_date_for_detail: Optional[str] = None,  # 'YYYY-MM-DD'
        detail_pnl_query_template: Optional[str] = None,
    ) -> None:
        # --- Store configuration
        self.db = db
        self.pnl_sql_path = pnl_sql_path
        self.pos_sql_path = pos_sql_path
        self.mapping_path = mapping_path
        self.mapping_sheet = mapping_sheet

        self.vol_books = vol_books or ['HNAT', 'HPHM', 'HREC', 'TREC']
        self.northeast_books = northeast_books or ['HNEP', 'HNYK', 'HPHM', 'HPJR', 'HREC', 'TREC']

        self.as_of_date_for_detail = as_of_date_for_detail
        self.detail_pnl_query_template = detail_pnl_query_template

        # --- Public data holders
        self.pos_df: pd.DataFrame = pd.DataFrame()
        self.pnl_df: pd.DataFrame = pd.DataFrame()
        self.mapping_df: pd.DataFrame = pd.DataFrame()
        self.pos_dict: Dict[str, pd.DataFrame] = {}
        self.pos_nd: Dict[str, pd.DataFrame] = {}
        self.rec_pnl_pivot: pd.DataFrame = pd.DataFrame()
        self.pjm_pos_disc: pd.DataFrame = pd.DataFrame()
        self.pjm_pos_nd: pd.DataFrame = pd.DataFrame()
        self.pos_level_pnl: pd.DataFrame = pd.DataFrame()

        # --- Execute the pipeline
        if run_on_init:
            self._load_queries()
            self._load_mapping()
            self._execute_core_queries()
            self._build_summaries()
            self._maybe_load_detailed_pnl()

    # -------------------------
    # Internal helpers
    # -------------------------
    def _load_queries(self) -> None:
        if not os.path.exists(self.pnl_sql_path):
            raise FileNotFoundError(f"pnl_sql_path not found: {self.pnl_sql_path}")

        with open(self.pnl_sql_path, "r", encoding="utf-8") as f:
            self.pnl_query = f.read()
        
        if not os.path.exists(self.pos_sql_path):
            raise FileNotFoundError(f"pos_sql_path not found: {self.pos_sql_path}")
        with open(self.pos_sql_path, "r", encoding="utf-8") as f:
            self.pos_query = f.read()


    def _load_mapping(self) -> None:
        if not os.path.exists(self.mapping_path):
            raise FileNotFoundError(f"mapping_path not found: {self.mapping_path}")

        # force openpyxl engine for xlsx
        self.mapping_df = pd.read_excel(
            self.mapping_path,
            sheet_name=self.mapping_sheet,
            engine="openpyxl"
        )

        # Basic sanity: expected 'MARKET' column for joining
        if 'MARKET' not in self.mapping_df.columns:
            # Try to normalize column names
            cols_norm = {c: c.strip().upper() for c in self.mapping_df.columns}
            self.mapping_df.rename(columns=cols_norm, inplace=True)
        if 'MARKET' not in (c.upper() for c in self.mapping_df.columns):
            raise ValueError("mapping_df must include a 'MARKET' column for merging.")

    def execute_znet_query(self, query: str) -> pd.DataFrame:
        if not self.db.oracle_conn_str:
            raise ValueError("Oracle connection string not provided in DbConfig.")
        try:
            with pyodbc.connect(self.db.oracle_conn_str) as conn:
                df = pd.read_sql(query, conn)
            return df
        except Exception as e:
            raise RuntimeError(f"Failed to execute SQL on Oracle: {e}") from e
        
    def execute_mssql_query(self, query: str) -> pd.DataFrame:
        try:
            with pyodbc.connect(self.db.mssql_conn_str) as conn:
                df = pd.read_sql(query, conn)
            return df
        except Exception as e:
            raise RuntimeError(f"Failed to execute SQL on MSSQL: {e}") from e
        

    def _execute_core_queries(self) -> None:
        # Use pandas.read_sql for cleaner code and column names
        try:
            with pyodbc.connect(self.db.mssql_conn_str) as conn:
                self.pos_df = pd.read_sql(self.pos_query, conn)
                self.pnl_df = pd.read_sql(self.pnl_query, conn)
        except Exception as e:
            raise RuntimeError(f"Failed to execute SQL on MSSQL: {e}") from e

        # Merge mapping onto pos_df (left join on MARKET)
        # Normalize for safe merge if needed
        if 'MARKET' not in self.pos_df.columns:
            cols_norm = {c: c.strip().upper() for c in self.pos_df.columns}
            self.pos_df.rename(columns=cols_norm, inplace=True)

        # Find correct MARKET column in mapping_df (case-insensitive)
        md_cols = {c.upper(): c for c in self.mapping_df.columns}
        pd_cols = {c.upper(): c for c in self.pos_df.columns}
        mkt_map_col = md_cols.get('MARKET')
        mkt_pos_col = pd_cols.get('MARKET')
        if mkt_map_col is None or mkt_pos_col is None:
            raise ValueError("Cannot merge mapping: 'MARKET' column missing in one of the dataframes.")

        self.pos_df = self.pos_df.merge(
            self.mapping_df,
            left_on=mkt_pos_col,
            right_on=mkt_map_col,
            how='left'
        )

        # Normalize YEAR to int where possible
        if 'YEAR' in self.pos_df.columns:
            self.pos_df['YEAR'] = pd.to_numeric(self.pos_df['YEAR'], errors='coerce').astype('Int64')
        if 'YEAR' in self.pnl_df.columns:
            self.pnl_df['YEAR'] = pd.to_numeric(self.pnl_df['YEAR'], errors='coerce').astype('Int64')

    def _build_summaries(self) -> None:
        # --- Voluntary book filter: exclude NYISO, PJM, NEPOOL; SOURCE != 'CP'
        required_cols = ['BOOK', 'ISO', 'SOURCE', 'TYPE', 'YEAR', 'DELTA', 'DELTA_ND']
        missing = [c for c in required_cols if c not in self.pos_df.columns]
        if missing:
            raise ValueError(f"pos_df missing required columns: {missing}")

        vol_mask = (
            self.pos_df['BOOK'].isin(self.vol_books) &
            (~self.pos_df['ISO'].isin(['NYISO', 'PJM', 'NEPOOL'])) &
            (self.pos_df['SOURCE'] != 'CP')
        )
        vol_book = self.pos_df.loc[vol_mask].copy()

        self.pos_dict['voluntary'] = vol_book.pivot_table(
            index='TYPE', columns='YEAR', values='DELTA', aggfunc='sum', fill_value=0.0
        )
        self.pos_nd['voluntary'] = vol_book.pivot_table(
            index='TYPE', columns='YEAR', values='DELTA_ND', aggfunc='sum', fill_value=0.0
        )

        # Add totals (row + column) safely
        for dct_name, pivot in [('pos_dict.voluntary', self.pos_dict['voluntary']),
                                ('pos_nd.voluntary', self.pos_nd['voluntary'])]:
            # Work on a copy to avoid pandas SettingWithCopy warnings
            p = pivot.copy()
            p.loc['Total'] = p.sum(numeric_only=True)
            p['Total'] = p.sum(axis=1, numeric_only=True)
            if dct_name.startswith('pos_dict'):
                self.pos_dict['voluntary'] = p
            else:
                self.pos_nd['voluntary'] = p

        # --- PJM positions (discounted and non-discounted)
        pjm_mask = (
            self.pos_df['BOOK'].isin(self.northeast_books) &
            (self.pos_df['ISO'] == 'PJM')
        )
        pjm_book = self.pos_df.loc[pjm_mask].copy()

        idx_cols = ['TYPE', 'MAPPING'] if 'MAPPING' in pjm_book.columns else ['TYPE']
        self.pjm_pos_disc = pjm_book.pivot_table(
            index=idx_cols, columns='YEAR', values='DELTA', aggfunc='sum', fill_value=0.0
        )
        self.pjm_pos_nd = pjm_book.pivot_table(
            index=idx_cols, columns='YEAR', values='DELTA_ND', aggfunc='sum', fill_value=0.0
        )

        # --- REC P&L (ATTRIBUTE == 'REC' and YEAR != 2020)
        if 'ATTRIBUTE' not in self.pnl_df.columns or 'PL_DAILY_NPV_NET_C' not in self.pnl_df.columns or 'BOOK' not in self.pnl_df.columns:
            raise ValueError("pnl_df missing required columns: ATTRIBUTE, PL_DAILY_NPV_NET_C, BOOK")

        pnl_mask = (self.pnl_df['ATTRIBUTE'] == 'REC') & (self.pnl_df['YEAR'] != 2020)
        rec_pnl = self.pnl_df.loc[pnl_mask].copy()

        self.rec_pnl_pivot = rec_pnl.pivot_table(
            index='BOOK', columns='YEAR', values='PL_DAILY_NPV_NET_C', aggfunc='sum', fill_value=0.0
        )
        # Add totals
        self.rec_pnl_pivot.loc['Total'] = self.rec_pnl_pivot.sum(numeric_only=True)
        self.rec_pnl_pivot['Total'] = self.rec_pnl_pivot.sum(axis=1, numeric_only=True)

    def _maybe_load_detailed_pnl(self) -> None:
        """Optionally load position-level detailed P&L with a date filter."""
        if not self.as_of_date_for_detail or not self.detail_pnl_query_template:
            return
        query = self.detail_pnl_query_template.format(AS_OF_DATE=self.as_of_date_for_detail)

        try:
            with pyodbc.connect(self.db.mssql_conn_str) as conn:
                self.pos_level_pnl = pd.read_sql(query, conn)
        except Exception as e:
            # Keep going even if this optional step fails
            self.pos_level_pnl = pd.DataFrame()
            print(f"[WARN] Detailed P&L query failed: {e}")

    # -------------------------
    # Convenience getters
    # -------------------------
    def get_voluntary_tables(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Return (discounted, non-discounted) voluntary pivot tables."""
        return self.pos_dict.get('voluntary', pd.DataFrame()), self.pos_nd.get('voluntary', pd.DataFrame())

    def close(self) -> None:
        """No persistent handles kept; provided for symmetry/compat."""
        return
    
    def reload_queries(self) -> None:
        """Re-run the entire data loading and processing pipeline."""
        self._load_queries()
        self._load_mapping()
        self._execute_core_queries()
        self._build_summaries()
        self._maybe_load_detailed_pnl()
        return None


# -------------------------
# Example usage (put this in your runner script, not inside the module)
# -------------------------
#if __name__ == "__main__":
    def initialize_state(self):
        # Build connection string(s)
        server = 'eemnaproddb'
        database = 'MidOfficeReporting'
        driver = '{ODBC Driver 17 for SQL Server}'  # or '{ODBC Driver 18 for SQL Server}'
        conn_str_mssql = (
            f"DRIVER={driver};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"Trusted_Connection=yes;"
            f"TrustServerCertificate=yes;"
        )

        # Optional Oracle (not used in this pipeline)
        conn_str_oracle = (
            "DRIVER={Oracle in OraClient12Home1};"
            "DBQ=//pdal1orac02.d90.tes.local:1521/zainet;"
            "Uid=Tracread;"
            "Pwd=sungard;"
        )

        db_cfg = DbConfig(
            mssql_conn_str=conn_str_mssql,
            oracle_conn_str=conn_str_oracle
        )

        pnl_sql_path = "./sql/eemna_pnl.sql"
        pos_sql_path = "./sql/eemna_position.sql"
        mapping_path = r"M:\Dept\TESI\Supply\Position Management\REC\POWER BI\Curve Mapping - IRIS vs ALIGNE.xlsx"
        mapping_path = "./data/Curve Mapping - IRIS vs ALIGNE.xlsx"

        # Optional detailed P&L query (parameterized with AS_OF_DATE)
        detailed_query_template = """
        SELECT *
        FROM [MidOfficeReporting].[Zainet].[Engie_PL_Detailed_EOD]
        WHERE AS_OF_DATE = '{AS_OF_DATE}'
        AND MRKT_ATTR1 = 'REC';
        """

        self.db=db_cfg
        self.pnl_sql_path=pnl_sql_path
        self.pos_sql_path=pos_sql_path
        self.mapping_path=mapping_path
        self.mapping_sheet="ALIGNE"
        self.vol_books=['HNAT', 'HPHM', 'HREC', 'TREC']
        self.northeast_books=['HNEP', 'HNYK', 'HPHM', 'HPJR', 'HREC', 'TREC']
        self.as_of_date_for_detail="2026-02-24"
        self.detail_pnl_query_template=detailed_query_template
        
        self.reload_queries()
        # Access objects
        #self.disc_vol, self.nond_vol = self.rec_data.get_voluntary_tables()
        """
        print("Voluntary (Discounted) head:\n", self.disc_vol.head())
        print("Voluntary (Non-Discounted) head:\n", self.nond_vol.head())
        print("REC P&L Pivot head:\n", self.rec_data.rec_pnl_pivot.head())
        print("PJM Discounted head:\n", self.rec_data.pjm_pos_disc.head())
        print("PJM Non-Discounted head:\n", self.rec_data.pjm_pos_nd.head())
        print("Detailed P&L rows:", len(self.rec_data.pos_level_pnl))
        """
        return None
    

if __name__ == "__main__":
    # %%
    data_fetcher = RecOpsData()
    data_fetcher.initialize_state()
    # %%
    data_fetcher.pnl_df.to_clipboard()

    # print hello world
    