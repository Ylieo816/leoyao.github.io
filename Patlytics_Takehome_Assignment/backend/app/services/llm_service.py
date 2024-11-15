import openai

def analyze_infringement_llm(patent, product):
    # Set up OpenAI API key, I use my API for sample
    openai.api_key = 'your_api_key_here'
    
    # Prepare the prompt for the LLM
    prompt = f"""Analyze potential patent infringement:
                Patent Title: {patent['title']}
                Patent Claims: {patent['claims']}
                Product Name: {product['name']}
                Product Description: {product['description']}

                Please provide an analysis in the following format:
                Likelihood: (High/Moderate/Low)
                Relevant Claims: (list of claim numbers that might be infringed)
                Explanation: (brief explanation of why the product might infringe the patent)
                """
    
    # Make a request to the OpenAI API
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a patent analysis expert. Analyze the potential infringement based on the given patent and product information."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    
    # Return the content of the LLM's response
    return response.choices[0].message.content