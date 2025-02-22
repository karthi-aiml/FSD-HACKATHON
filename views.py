from django.shortcuts import render
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Embedded schema and data
SCHEMA = {
    "tables": [
        {
            "name": "sales",
            "columns": [
                {"name": "sale_id", "type": "int"},
                {"name": "region", "type": "varchar"},
                {"name": "amount", "type": "float"},
                {"name": "date", "type": "date"},
                {"name": "customer_id", "type": "int"},
                {"name": "product_id", "type": "int"}
            ]
        },
        {
            "name": "customers",
            "columns": [
                {"name": "customer_id", "type": "int"},
                {"name": "name", "type": "varchar"},
                {"name": "email", "type": "varchar"},
                {"name": "region", "type": "varchar"},
                {"name": "join_date", "type": "date"}
            ]
        }
    ]
}

DATA = {
    "sales": [
        {
            "sale_id": 1,
            "region": "North",
            "amount": 100.0,
            "date": "2023-09-01",
            "customer_id": 1,
            "product_id": 101
        },
        {
            "sale_id": 2,
            "region": "South",
            "amount": 200.0,
            "date": "2023-09-15",
            "customer_id": 2,
            "product_id": 102
        }
    ],
    "customers": [
        {
            "customer_id": 1,
            "name": "Johny",
            "email": "johny@gmail.com",
            "region": "North",
            "join_date": "2022-06-01"
        },
        {
            "customer_id": 2,
            "name": "Lilly",
            "email": "lilly@gmail.com",
            "region": "South",
            "join_date": "2023-01-01"
        }
    ]
}

def extract_keywords(query):
    """
    Extract keywords from the query.
    """
    # For simplicity, split the query into words and remove stopwords
    stopwords = {"the", "and", "for", "with", "me", "show", "data"}
    keywords = [word.lower() for word in query.split() if word.lower() not in stopwords]
    return keywords

def match_schema(query, schema):
    """
    Match the query with the schema to find relevant tables.
    """
    # Extract keywords from the query
    keywords = extract_keywords(query)
    
    # Preprocess the schema
    table_descriptions = []
    for table in schema['tables']:
        columns = ", ".join([col['name'] for col in table['columns']])
        table_descriptions.append(f"{table['name']}: {columns}")
    
    # Compute TF-IDF vectors for the query and table descriptions
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([" ".join(keywords)] + table_descriptions)
    
    # Compute cosine similarity between the query and each table description
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    # Filter tables with similarity above a threshold
    relevant_tables = {}
    threshold = 0.2  # Adjust this threshold as needed
    for i, similarity in enumerate(cosine_similarities):
        if similarity > threshold:
            table = schema['tables'][i]
            relevant_tables[table['name']] = {
                'relevance_score': similarity,
                'columns': table['columns']
            }
    
    return relevant_tables

def home(request):
    """
    Handle the home page and process user queries.
    """
    try:
        if request.method == 'POST':
            query = request.POST.get('query')
            if not query:
                raise ValueError("Query cannot be empty.")
            
            # Match the query with the schema
            relevant_tables = match_schema(query, SCHEMA)
            
            # Filter data based on relevant tables
            filtered_data = {}
            for table_name in relevant_tables:
                if table_name in DATA:
                    filtered_data[table_name] = DATA[table_name]
            
            # Render the results page
            return render(request, 'selector/results.html', {
                'query': query,
                'tables': relevant_tables,
                'data': filtered_data
            })
        
        # Render the home page for GET requests
        return render(request, 'selector/home.html')
    
    except Exception as e:
        return render(request, 'selector/error.html', {
            'error_message': str(e)
        })