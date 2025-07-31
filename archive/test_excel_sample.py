"""
Create a sample Excel file for testing
"""
import pandas as pd
import os

def create_sample_excel():
    """Create a sample Excel file with financial data"""
    
    # Sample financial data
    bilan_data = {
        'Compte': [
            'Total Actif',
            'Immobilisations nettes', 
            'Stocks',
            'Créances clients',
            'Trésorerie',
            'Capitaux propres',
            'Dettes financières',
            'Dettes court terme'
        ],
        'Montant': [
            1000000,  # Total Actif
            500000,   # Immobilisations
            200000,   # Stocks
            150000,   # Créances
            150000,   # Trésorerie
            400000,   # Capitaux propres
            300000,   # Dettes financières
            300000    # Dettes CT
        ]
    }
    
    cr_data = {
        'Compte': [
            'Chiffre d\'affaires',
            'Résultat d\'exploitation',
            'Résultat net',
            'Charges personnel'
        ],
        'Montant': [
            1200000,  # CA
            100000,   # Résultat exploitation
            75000,    # Résultat net
            250000    # Charges personnel
        ]
    }
    
    # Create Excel file with multiple sheets
    excel_file = 'sample_financial_data.xlsx'
    
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        pd.DataFrame(bilan_data).to_excel(writer, sheet_name='Bilan', index=False)
        pd.DataFrame(cr_data).to_excel(writer, sheet_name='CR', index=False)
    
    print(f"Sample Excel file created: {excel_file}")
    print(f"File size: {os.path.getsize(excel_file)} bytes")
    
    # Display contents
    print("\nBilan data:")
    print(pd.DataFrame(bilan_data))
    
    print("\nCR data:")
    print(pd.DataFrame(cr_data))

if __name__ == "__main__":
    create_sample_excel()