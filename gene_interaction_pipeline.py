import requests
import networkx as nx
import matplotlib.pyplot as plt


def fetch_gene_interactions(gene_name):
    """
    Fetch interaction data for a specified gene from BioGRID API.

    Args:
        gene_name (str): The name of the gene to query.

    Returns:
        dict: A dictionary of interactions if found, else None.
    """
    print("\nFetching gene interactions from BioGRID...")

    url = "https://webservice.thebiogrid.org/interactions"
    api_key = "ASK FOR AND USE YOUR KEY ACCESS"

    params = {
        "searchNames": "true",
        "geneList": gene_name,
        "format": "json",
        "includeInteractors": "true",
        "accesskey": api_key,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Check for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

    print(f"API URL: {response.url}")

    if response.status_code == 200:
        try:
            data = response.json()
            if not data:
                print("No interaction data found for the given gene.")
            else:
                print("Data successfully retrieved!")
                print(f"Available keys in the response: {list(data.keys())[:10]}")
            return data
        except ValueError:
            print("Error parsing response as JSON.")
            print("Response Text:", response.text)
    else:
        print(f"Error fetching data from BioGRID: {response.status_code}")
        print("Response Text:", response.text)

    return None


def extract_interactors(details):
    """
    Extract interactors from interaction details.

    Args:
        details (dict): A dictionary containing interaction details.

    Returns:
        tuple: Interactor A, Interactor B names, and quantitation if available.
    """
    # May need adjustment based on API response
    interactor_a = details.get("OFFICIAL_SYMBOL_A") or details.get("InteractorA")
    interactor_b = details.get("OFFICIAL_SYMBOL_B") or details.get("InteractorB")
    quantitation = details.get("QUANTITATION")  
    return interactor_a, interactor_b, quantitation


import matplotlib.patches as mpatches

def plot_interaction_network(interactions, gene_name):
    """
    Visualize gene interaction network using NetworkX.

    Args:
        interactions (dict): Interaction data returned by the BioGRID API.
        gene_name (str): The queried gene name.
    """
    G = nx.DiGraph()

    # Add the queried gene as the central node
    G.add_node(gene_name, color="orange", size=1200, label=gene_name)

    for interaction_id, details in interactions.items():
        interactor_a, interactor_b, quantitation = extract_interactors(details)

        if interactor_a and interactor_b:
            # Validate quantitation before processing
            try:
                quantitation = float(quantitation) if quantitation not in [None, "-"] else None
            except ValueError:
                quantitation = None

            # Determine color based on quantitation and queried gene status
            def get_node_color(interactor):
                if interactor == gene_name:
                    return "orange"
                if quantitation is not None:
                    return (
                        "springgreen" if quantitation > 0 else
                        "lightcoral" if quantitation < 0 else
                        "lightblue"
                    )
                return "lightblue"

            # Add nodes with colors determined
            G.add_node(interactor_a, color=get_node_color(interactor_a), size=500)
            G.add_node(interactor_b, color=get_node_color(interactor_b), size=500)
            G.add_edge(interactor_a, interactor_b)

    if len(G.edges) == 0:
        print("No valid edges found in the interaction data.")
        return

    # Extract node attributes for visualization
    node_colors = [G.nodes[node].get("color", "orange") for node in G.nodes]
    node_sizes = [G.nodes[node].get("size", 300) for node in G.nodes]

    # Draw the graph
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=node_sizes,
        font_size=10,
        edge_color="gray",
        arrows=True,
    )
    plt.title(f"Interaction Network for Gene: {gene_name}")

    # Add legend
    legend_elements = [
        mpatches.Patch(color="orange", label="Queried Gene"),
        mpatches.Patch(color="springgreen", label="Positive Interaction (Quantitation > 0)"),
        mpatches.Patch(color="lightcoral", label="Negative Interaction (Quantitation < 0)"),
        mpatches.Patch(color="lightblue", label="Neutral/Unknown Interaction (Quantitation = 0 or Missing)")
    ]
    plt.legend(handles=legend_elements, loc="upper right", fontsize=10)

    plt.show()


if __name__ == "__main__":
    gene_name = input("Enter the gene name (e.g., fimH): ").strip()
    interactions = fetch_gene_interactions(gene_name)

    if interactions:
        print(f"\nNumber of interactions found: {len(interactions)}\n")
        for interaction_id, details in list(interactions.items())[:10]:  # Display first 10 interactions
            interactor_a, interactor_b, quantitation = extract_interactors(details)
            print(f"Interaction ID: {interaction_id}")
            print(f"Interactor A: {interactor_a or 'N/A'}")
            print(f"Interactor B: {interactor_b or 'N/A'}")
            print(f"Quantitation: {quantitation or 'N/A'}\n")

        plot_interaction_network(interactions, gene_name)
    else:
        print("No interactions to display.")
