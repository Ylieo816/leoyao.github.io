import json
from app.services.llm_service import analyze_infringement_llm

def check_infringement(patent_id: str, company_name: str):
    """
    Check for potential patent infringement by a company.
    """
    print(f"Processing infringement check for patent_id={patent_id}, company_name={company_name}")
    
    try:
        # Load patent and company data
        patents = json.load(open('data/patents.json'))
        companies = json.load(open('data/company_products.json'))
        
        # Find relevant patent
        patent = next((p for p in patents if p['publication_number'] == patent_id), None)
        if not patent:
            return {'error': 'Patent not found'}
        
        # Find relevant company
        company = next((c for c in companies['companies'] if company_name in c['name']), None)
        if not company:
            return {'error': 'Company not found'}
        
        # Analyze potential infringement
        analysis = analyze_infringement(patent, company)
        print(f"Analysis completed for {company_name}")
        return analysis
    
    except Exception as e:
        print(f"An error occurred during infringement check: {str(e)}")
        return {'error': 'An internal error occurred'}

def analyze_infringement(patent, company):
    """
    Analyze potential infringement for each product of the company.
    """
    infringing_products = []
    
    for product in company['products']:
        # Analyze each product using LLM
        analysis = analyze_infringement_llm(patent, product)
        
        # Parse LLM output
        likelihood, relevant_claims, explanation = parse_llm_output(analysis)
        
        infringing_products.append({
            'product_name': product['name'],
            'infringement_likelihood': likelihood,
            'relevant_claims': relevant_claims,
            'explanation': explanation
        })
    
    # Sort products by number of relevant claims
    sorted_products = sorted(infringing_products, 
                             key=lambda x: len(x['relevant_claims']), 
                             reverse=True)
    
    # Return top two most likely infringing products
    return sorted_products[:2]

def parse_llm_output(llm_output):
    """
    Parse the output from the LLM analysis.
    """
    lines = llm_output.split('\n')
    likelihood, relevant_claims, explanation = "Unknown", [], ""
    
    for line in lines:
        if line.startswith("Likelihood:"):
            likelihood = line.split(":")[1].strip()
        elif line.startswith("Relevant Claims:"):
            relevant_claims = line.split(":")[1].strip().split(", ")
        elif line.startswith("Explanation:"):
            explanation = line.split(":")[1].strip()
    
    return likelihood, relevant_claims, explanation