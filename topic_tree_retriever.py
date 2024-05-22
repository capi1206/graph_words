import spacy
import nltk
import networkx as nx
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
nltk.download('stopwords')
import prompting

nlp = spacy.load("it_core_news_lg")
italian_stopwords = stopwords.words('italian')

# Download stopwords data
#nltk.download('stopwords')


def identify_entities(query):
    # Tokenize the query using spaCy
    doc = nlp(query)

    entities = [token.text for token in doc if token.ent_type_ != '' or
                 (token.pos_ == 'NOUN' and token.text.lower() not in italian_stopwords)]
    n_entities =[ent.text for ent in doc.ents]
    relations = []
    for token in doc:
        if token.head.text in entities and token.text in entities: #token.dep_ in ['prep', 'pobj']:  # Check if the token is a preposition or object of preposition
            relations.append((token.head.text, token.text, token.dep_)) 
    
    return entities, n_entities, relations

def create_entity_tree(n_entities, relations):
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add nodes for named entities
    for entity in n_entities:
        G.add_node(entity, color='red')
    
    # Add nodes for other entities and create edges based on relations
    for head, tail, label in relations:
        G.add_node(tail, color='blue')
        G.add_edge(head, tail, label=label)
    
    return G

def visualize_tree(G):
    pos = nx.spring_layout(G)
    colors = [G.nodes[node]['color'] for node in G.nodes]
    labels = nx.get_edge_attributes(G, 'label')
    
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=3000, font_size=10, font_color='white', font_weight='bold', edge_color='black')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='red')
    plt.show()

#query = input("Enter a text: ")

# Identify entities in the entered text
entities, n_entities, relations= identify_entities(query)

# Print the identified entities
#print("Entities:", entities)
#print("Named entities:", n_entities)
#print("Relations:",relations)

#G = create_entity_tree(n_entities, relations)

# Visualize the entity tree
#visualize_tree(G)
print(prompting)