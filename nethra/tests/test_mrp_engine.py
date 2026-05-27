import unittest
import os
import pandas as pd
import numpy as np
from src.mrp_engine import MRPEngine

class TestMRPEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Sets up the MRPEngine instance using the generated prototype datasets."""
        cls.engine = MRPEngine()

    def test_data_loaded_successfully(self):
        """Verify that the frame and covariates were successfully loaded into Pandas DataFrames."""
        self.assertIsNotNone(self.engine.df_frame, "Poststratification frame failed to load.")
        self.assertIsNotNone(self.engine.df_covariates, "Booth covariates failed to load.")
        self.assertGreater(len(self.engine.df_frame), 0, "Poststratification frame is empty.")
        self.assertGreater(len(self.engine.df_covariates), 0, "Booth covariates DataFrame is empty.")

    def test_k_anonymity_suppression(self):
        """
        Verify that the k-anonymity gate successfully suppresses and merges all cells under 10
        to remain 100% compliant with the India DPDP Act 2023.
        """
        k_val = 10
        
        # Count cells under k before merging in the raw frame
        raw_sparse_count = (self.engine.df_frame['n_voters'] < k_val).sum()
        self.assertGreater(raw_sparse_count, 0, "Raw test frame should contain sparse cells to validate the gate.")
        
        # Enforce k-anonymity
        df_clean = self.engine.enforce_k_anonymity(k=k_val)
        
        # Count cells under k after enforcement
        clean_sparse_count = (df_clean['n_voters'] < k_val).sum()
        self.assertEqual(clean_sparse_count, 0, f"DPDP Violations! {clean_sparse_count} cells under k={k_val} remain after merging.")
        
        # Verify that total voters are preserved across the process
        total_voters_raw = self.engine.df_frame['n_voters'].sum()
        total_voters_clean = df_clean['n_voters'].sum()
        self.assertEqual(total_voters_raw, total_voters_clean, "Voter population count mismatch after anonymity merging!")

    def test_mrp_projection_math(self):
        """
        Verify that the MRP projection output is mathematically consistent.
        Assert that the sum of projected swing votes equals the rounded expectation sum(N_k * P_k).
        """
        df_strat, df_results = self.engine.run_mrp_projection(loss_aversion_mult=1.8, baseline_swing_prior=0.35, k_anon=10)
        
        # Calculate mathematical expectation on the strata frame
        expected_strata_swings = np.round(df_strat['n_voters'] * df_strat['swing_prob']).astype(int).sum()
        actual_strata_swings = df_strat['swing_votes'].sum()
        self.assertEqual(actual_strata_swings, expected_strata_swings, "Strata-level projected swing votes do not match expectation.")
        
        # Verify that total voters across results matches the poststratification total
        total_voters_strat = df_strat['n_voters'].sum()
        total_voters_results = df_results['total_voters'].sum()
        self.assertEqual(total_voters_results, total_voters_strat, "Booth aggregated voter counts mismatch poststratification total.")
        
        # Verify that swing votes align
        total_swings_strat = df_strat['swing_votes'].sum()
        total_swings_results = df_results['swing_votes'].sum()
        self.assertEqual(total_swings_results, total_swings_strat, "Booth aggregated swing votes mismatch poststratification total.")

    def test_spatial_bridge(self):
        """Verify that the Voronoi spatial bridge overlays booth coordinates onto village wards correctly."""
        _, df_results = self.engine.run_mrp_projection()
        df_joined = self.engine.spatial_bridge_join(df_results)
        
        self.assertIn('spatial_ward', df_joined.columns, "Spatial ward mapping column missing in output.")
        self.assertIn('ward_infra_score', df_joined.columns, "Spatial infrastructure score column missing.")
        self.assertFalse(df_joined['spatial_ward'].isnull().any(), "Some booths failed to match spatial ward overlays.")
        
        # Verify specific centroid assignment for Cantt Area (Booth 7 lat: 26.8185, lon: 80.9525)
        booth_7 = df_joined[df_joined['booth_id'] == 7].iloc[0]
        self.assertEqual(booth_7['spatial_ward'], "Lucknow Cantt Cantonment", "Booth 7 spatial assignment incorrect.")

    def test_cadre_anomaly_detection(self):
        """Verify that anomaly scoring calculates deltas between predictions and cadre survey baselines."""
        _, df_results = self.engine.run_mrp_projection()
        df_results = self.engine.spatial_bridge_join(df_results)
        df_anomaly, cadre_support = self.engine.calculate_cadre_anomaly(df_results)
        
        self.assertIn('cadre_support', df_anomaly.columns, "Cadre support baseline column missing.")
        self.assertIn('anomaly_score', df_anomaly.columns, "Anomaly score delta column missing.")
        self.assertTrue((df_anomaly['anomaly_score'] >= 0.0).all(), "Negative anomaly delta scores detected.")

if __name__ == '__main__':
    unittest.main()
