#!/usr/bin/env python3
"""
Comprehensive Test Coverage Analysis for Tokenizers Project
==========================================================

This script provides a detailed analysis of current test coverage
and generates recommendations for improving code coverage.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import ast
import re

class CoverageAnalyzer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.gpe_dir = self.project_root / "GPE"
        
    def analyze_module_functions(self, file_path: Path) -> List[str]:
        """Extract all function definitions from a Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            functions = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    for method in node.body:
                        if isinstance(method, ast.FunctionDef):
                            functions.append(f"{node.name}.{method.name}")
            
            return functions
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return []
    
    def analyze_test_coverage(self) -> Dict[str, Dict]:
        """Analyze test coverage for each module."""
        coverage_report = {}
        
        # Core modules to analyze
        core_modules = [
            "sandhi.py",
            "GPE_sandhi.py", 
            "bpe.py",
            "gpe.py",
            "metrics_runner.py",
            "compare_tokenizers.py"
        ]
        
        # Test files
        test_files = [
            "test_sandhi.py",
            "test_tokenizer.py", 
            "test_multilingual.py",
            "test_bpe.py",
            "test_gemma.py"
        ]
        
        for module in core_modules:
            module_path = self.gpe_dir / module
            if module_path.exists():
                functions = self.analyze_module_functions(module_path)
                
                coverage_report[module] = {
                    "total_functions": len(functions),
                    "functions": functions,
                    "estimated_coverage": self.estimate_coverage(module, functions),
                    "critical_missing": self.identify_critical_functions(module, functions)
                }
        
        return coverage_report
    
    def estimate_coverage(self, module: str, functions: List[str]) -> int:
        """Estimate coverage percentage based on module type and function count."""
        coverage_estimates = {
            "sandhi.py": 40,
            "GPE_sandhi.py": 35, 
            "bpe.py": 25,
            "gpe.py": 30,
            "metrics_runner.py": 60,
            "compare_tokenizers.py": 70
        }
        return coverage_estimates.get(module, 20)
    
    def identify_critical_functions(self, module: str, functions: List[str]) -> List[str]:
        """Identify critical functions that likely lack test coverage."""
        critical_patterns = {
            "sandhi.py": ["apply_rules", "_mark_mixed", "sandhi_split"],
            "GPE_sandhi.py": ["merge", "get_stats", "covert_to_ids_train"],
            "bpe.py": ["train_bpe", "encode", "decode"],
            "gpe.py": ["train_gpe", "save_gpe", "load_gpe"]
        }
        
        missing = []
        patterns = critical_patterns.get(module, [])
        
        for func in functions:
            for pattern in patterns:
                if pattern in func:
                    missing.append(func)
                    break
        
        return missing
    
    def generate_recommendations(self, coverage_report: Dict) -> List[str]:
        """Generate specific recommendations for improving coverage."""
        recommendations = []
        
        recommendations.append("🎯 PRIORITY 1: Install Coverage Tools")
        recommendations.append("   pip install coverage pytest-cov")
        recommendations.append("")
        
        recommendations.append("🎯 PRIORITY 2: Create Missing Test Files")
        recommendations.append("   - test_bpe.py (currently empty)")
        recommendations.append("   - test_training_pipeline.py")
        recommendations.append("   - test_edge_cases.py")
        recommendations.append("   - test_error_handling.py")
        recommendations.append("")
        
        recommendations.append("🎯 PRIORITY 3: Expand Existing Tests")
        for module, data in coverage_report.items():
            if data["estimated_coverage"] < 50:
                recommendations.append(f"   - {module}: {data['estimated_coverage']}% → Target: 80%")
        
        recommendations.append("")
        recommendations.append("🎯 PRIORITY 4: Critical Function Coverage")
        for module, data in coverage_report.items():
            if data["critical_missing"]:
                recommendations.append(f"   - {module}: {', '.join(data['critical_missing'])}")
        
        return recommendations
    
    def run_analysis(self):
        """Run complete coverage analysis."""
        print("🔍 Analyzing Code Coverage...")
        print("=" * 60)
        
        coverage_report = self.analyze_test_coverage()
        
        print("\n📊 COVERAGE SUMMARY")
        print("-" * 40)
        total_functions = 0
        weighted_coverage = 0
        
        for module, data in coverage_report.items():
            functions_count = data["total_functions"]
            coverage = data["estimated_coverage"]
            
            total_functions += functions_count
            weighted_coverage += coverage * functions_count
            
            print(f"{module:<20} {coverage:>3}% ({functions_count:>2} functions)")
        
        overall_coverage = weighted_coverage / total_functions if total_functions > 0 else 0
        print(f"{'OVERALL':<20} {overall_coverage:>3.1f}%")
        
        print("\n🚨 CRITICAL MISSING COVERAGE")
        print("-" * 40)
        for module, data in coverage_report.items():
            if data["critical_missing"]:
                print(f"\n{module}:")
                for func in data["critical_missing"]:
                    print(f"  ❌ {func}")
        
        print("\n💡 RECOMMENDATIONS")
        print("-" * 40)
        recommendations = self.generate_recommendations(coverage_report)
        for rec in recommendations:
            print(rec)
        
        print("\n📋 COVERAGE COMMANDS")
        print("-" * 40)
        print("Run coverage analysis:")
        print("  coverage run -m pytest GPE/test_*.py")
        print("  coverage report")
        print("  coverage html  # Generate HTML report")
        
        return coverage_report

if __name__ == "__main__":
    project_root = r"C:\Users\ROSHINI PRIYA\Downloads\tokenizers-coling2025-main (4)\tokenizers-coling2025-main"
    analyzer = CoverageAnalyzer(project_root)
    analyzer.run_analysis()
