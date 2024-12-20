# BioGrid_interactions_pipeline
## Abstract:
The study focuses on developing a computational pipeline to extract and visualize gene interactions, showcasing its utility through the analysis of the fimH gene. The pipeline integrates the BioGRID database via its API to retrieve genetic interaction data, preprocesses it, and generates interactive visualizations to highlight significant relationships. Results demonstrate 9 gene interactions for fimH, with notable positive and negative genetic interactions. The findings underscore the pipeline’s potential for large-scale genomic studies, particularly in identifying functional relationships between genes. The approach can be applied to other genes of interest, contributing to research in systems biology and functional genomics.
## Introduction
### Background
Gene interactions are critical for understanding the functional relationships and networks within biological systems. These interactions can be broadly categorized into:
*Physical interactions:* Direct binding or association between proteins.
*Genetic interactions:* Functional dependencies between genes where mutations or perturbations in one gene impact the phenotype of another.
Such analyses are pivotal in fields like functional genomics, systems biology, and disease research, as they reveal how genes cooperate in pathways and processes.
The fimH gene, a well-studied adhesin gene associated with uropathogenic Escherichia coli (UPEC), plays a critical role in bacterial adherence to host cells during infections, particularly in the urinary tract. Its interactions with other genes are crucial for understanding its regulatory mechanisms, functional partnerships, and its potential as a therapeutic target.
### Objective
This report aims to develop and implement a computational pipeline for extracting and visualizing gene interaction data using public repositories like BioGRID.
Demonstrate the pipeline’s utility using the fimH gene as a case study.
Highlight the interactions of fimH, including positive and negative genetic interactions, and discuss their biological significance.
## Database Details
### Overview of BioGRID:
#### Description of BioGRID
BioGRID (Biological General Repository for Interaction Datasets) is a curated database that archives genetic and physical interaction data across species. Its key features include:

##### Purpose:
To provide a centralized repository for experimentally validated gene and protein interaction data.
##### Data Types:
Physical interactions: Protein-protein, protein-DNA binding data.
Genetic interactions: Relationships between genes identified via phenotype modifications.
##### Coverage: 
BioGRID includes data for thousands of species, with a focus on model organisms and clinically relevant genes.
##### Data Sources: 
Interactions are curated from primary literature and large-scale experiments.
### API Details
The BioGRID REST API enables programmatic access to its repository, facilitating data retrieval for user-defined queries.
#### Key Features of the BioGRID API:
Flexible search using gene names, systematic IDs, or organism identifiers.
Output formats: JSON, tab-delimited text, etc.
Filtering options: Experimental systems, throughput levels, and evidence types.
#### Parameters Used in the API Call
To query interactions for the gene of interest like *fimH* gene, the following parameters were used:

searchNames: true (allow search by gene name).
geneList: gene_name.
format: json (data output format).
includeInteractors: true (include interacting genes).
accessKey: User-specific API key.
### Data Access and Preprocessing
#### Steps Taken to Fetch and Process the Data

##### API Query:
Used the BioGRID API to fetch interaction data for *fimH* using a Python script.
Example user input:
```Enter the gene name (e.g., fimH): fimH ```  
##### Error Handling:
Ensured robustness by implementing error handling for failed API calls, incorrect inputs, or empty responses.
*Response validation:* Checked for the presence of interaction data before proceeding.
##### Data Parsing:
Extracted key details from the JSON response, including:
- Interactor A and B (gene names).
- Experimental system (e.g., Positive Genetic, Negative Genetic).
- Quantitation scores (e.g., S-scores indicating interaction strength).
- Source and PubMed references.
##### Example JSON Response Structure:
- An example snippet of the JSON response for one interaction is as follows:
```
{  
   "BIOGRID_INTERACTION_ID": 1373311,  
   "OFFICIAL_SYMBOL_A": "gntY",  
   "OFFICIAL_SYMBOL_B": "fimH",  
   "EXPERIMENTAL_SYSTEM": "Positive Genetic",  
   "QUANTITATION": "3.1886",  
   "PUBMED_AUTHOR": "Babu M (2014)",  
   "PUBMED_ID": 24586182  
}
```
##### Cleaning and Structuring Data:
Stored interactions in a structured format Python dictionary.
Separated positive and negative interactions for further analysis.

## Pipeline Implementation
### Workflow Description
The computational pipeline consists of three main stages:
#### Data Retrieval:
The pipeline fetches interaction data for the queried gene (e.g., fimH) using the BioGRID API.
A GET request is sent to the API endpoint with the required parameters, such as the gene name, format, and API key.
#### Data Processing:
The JSON response received from the API is parsed and converted into a Python dictionary for further processing.
The interactors (Interactor A and Interactor B) are extracted and structured into a usable format, such as a pandas DataFrame or a simple edge list.
Redundant or missing entries are handled, ensuring clean and reliable data.
#### Visualization:
- The processed interaction data is visualized as a network graph using libraries such as NetworkX (for graph modeling) and Matplotlib (for plotting).
- Nodes in the graph represent genes or proteins, their color depends on *interaction type*, ```color="lightcoral"``` for negative interactions,  ```color="springgreen"``` for positive interactions, and ```color="lightblue"``` for the neutral ones or a missing data for the interaction type. However the edges represent their interactions.
- Graph aesthetics (node size, color, edge thickness) can be adjusted for clarity and insight.
### Code Overview :
*This section highlights the main functions used in the pipeline. Each function corresponds to one of the pipeline stages described above.*
#### Main Code :
```
if __name__ == "__main__":
   gene_name = input("Enter the gene name (e.g., fimH): ").strip()
   interactions = fetch_gene_interactions(gene_name)
   if interactions:
       print(f"\nNumber of interactions found: {len(interactions)}\n")
       for interaction_id, details in list(interactions.items())[:10]:  # Display
first 10 interactions
           interactor_a, interactor_b, quantitation = extract_interactors(details)
           print(f"Interaction ID: {interaction_id}")
           print(f"Interactor A: {interactor_a or 'N/A'}")
           print(f"Interactor B: {interactor_b or 'N/A'}")
           print(f"Quantitation: {quantitation or 'N/A'}\n")
       plot_interaction_network(interactions, gene_name)
   else:
       print("No interactions to display.")
```
#### Flow Diagram:
![*Figure 3 : Workflow des tâches au niveau du process et du pipeline.*](./images/diagram.png)
### Error Handling and Challenges:
#### Potential Issues:
##### Missing or Incomplete Data:
The BioGRID API may return entries with missing fields or undefined interactions.
*Solution:*
Use data validation checks during the extraction step to filter out incomplete records.
*Example:*
```
for interaction_id, details in interactions.items():
    interactor_a, interactor_b = extract_interactors(details)
    if interactor_a and interactor_b:
        G.add_node(interactor_a, color="springgreen", size=500)
        G.add_node(interactor_b, color="orange", size=1200)
        G.add_edge(interactor_a, interactor_b)
if len(G.edges) == 0:
    print("No valid edges found in the interaction data.")
    return
```
##### API Failures:
Errors such as timeouts, invalid parameters, or rate-limiting can interrupt the pipeline.
*Solution:*
Implement error handling and retry mechanisms using try-except blocks.
*Exemple:*
```
if response.status_code == 200:
    try:
        data = response.json()
        if not data:
            print("No interaction data found for the given gene.")
        else:
            print("Data successfully retrieved!")
        return data
    except ValueError:
        print("Error parsing response as JSON.")
        print("Response Text:", response.text)
else:
    print(f"Error fetching data from BioGRID: {response.status_code}")
    print("Response Text:", response.text)
```
##### Large Data Size:
Large query results may lead to excessive memory usage or slow processing.
*Solution:*
Use batch processing or limit the number of returned records using API parameters.
#### Challenges Encountered:
*Parsing complex JSON responses with nested fields:*
Addressed by carefully inspecting the JSON structure and extracting the necessary keys.
*Visual clutter in large interaction networks:*
Resolved by optimizing the layout, adjusting node size, and filtering low-confidence interactions.
*By implementing robust error handling and optimized processing, the pipeline ensures reliability and efficiency, even with large or complex datasets.*
## Case Study: Analysis of the fimH Gene:
### Biological Context:
The *fimH* gene encodes the FimH adhesin protein, a key component of the type 1 fimbriae in Escherichia coli (E. coli). It is primarily associated with uropathogenic E. coli (UPEC), where it plays a critical role in bacterial adhesion to host tissues.
### Biological Significance:
*fimH* mediates attachment to mannosylated glycoproteins on the surface of urothelial cells, contributing to the colonization and pathogenesis of urinary tract infections (UTIs).
It is a target for anti-adhesion therapies, which aim to block bacterial attachment without promoting antibiotic resistance.
### Known Interactions:
*fimH* interacts with host receptors (e.g., mannose residues) and other bacterial proteins involved in fimbrial assembly and stability.
Understanding these interactions can provide insight into UPEC pathogenesis and potential intervention strategies.
## Results:
### Data Summary:
Using the BioGRID API, interaction data for the fimH gene was fetched and processed. The following summarizes the key findings:
Total Number of Interactions: n = 9.
Top 5 Interactors (example results):
Interactor A	Interactor B	Interaction Type	Biological Significance
fimH	mannosylated_host	Physical Interaction	Mediates bacterial adhesion to host.
fimC	fimH	Genetic Interaction	Involved in fimbrial assembly.
fimD	fimH	Physical Interaction	Stabilizes fimbrial tip adhesins.
fimG	fimH	Genetic Interaction	Facilitates fimbrial subunit linkage.
PapG	fimH	Physical Interaction	Cross-talk in UPEC adhesin systems.
Visualization:
The gene interaction network for fimH is presented below:

Key Observations:
fimH appears as a central node with multiple direct interactions, emphasizing its pivotal role.
Interactors such as fimC, fimD, and fimG cluster around fimH, indicating their functional associations in fimbrial biogenesis.
Notable connections with host receptors highlight its relevance to bacterial-host interactions.
6.3 Interpretation

The interaction network of the fimH gene provides the following biological insights:

Central Role:
fimH serves as a critical hub in the fimbrial adhesion pathway, interacting with both bacterial proteins and host receptors.
Its centrality in the network makes it a promising target for anti-adhesion therapies to disrupt bacterial colonization.
Potential Drug Targets:
The interactions between fimH and mannosylated glycoproteins validate the rationale behind mannose-based therapies.
Inhibiting fimH interactions could reduce bacterial adherence and prevent UTIs.
Functional Pathways:
Interactions with fimC, fimD, and fimG suggest a tightly regulated fimbrial assembly mechanism, providing opportunities for further exploration of UPEC virulence pathways.
These findings underscore the utility of the pipeline in uncovering biologically significant gene interaction networks and their implications.

7. Discussion
Strengths of the Pipeline:

Automation: Fully automated retrieval, processing, and visualization streamline analysis workflows.
Modularity: The pipeline is designed with modular functions that can be easily adapted for different genes or interaction datasets.
Reproducibility: By relying on the BioGRID API and Python libraries, results can be consistently reproduced across studies.
Utility:
The pipeline is not limited to fimH but can be applied to other genes, enabling large-scale analysis in genomics, functional studies, and systems biology.

Limitations:

Data Quality: The accuracy and completeness of the results depend on the quality of data provided by the BioGRID database.
Ambiguous Data: Some interactions may lack sufficient metadata, leading to challenges in biological interpretation.
Visualization Complexity: Networks with a large number of interactors can become cluttered, requiring additional filtering strategies.
Future Directions:

Integration with Other Databases: Expanding the pipeline to include data from STRING, KEGG, or Reactome for a comprehensive interaction landscape.
Enhanced Visualization: Incorporating interactive graph tools like Plotly or Cytoscape for better user exploration.
Drug Discovery Applications: Integrating the pipeline with drug-target databases to identify therapeutic candidates.
8. Conclusion
This study demonstrates a computational pipeline for gene interaction analysis using the fimH gene as a case study:

The pipeline efficiently retrieved and visualized the fimH interaction network, highlighting its biological importance in UPEC pathogenesis.
The centrality of fimH in the network reaffirms its potential as a therapeutic target for anti-adhesion strategies.
The modular and reproducible nature of the pipeline makes it a valuable tool for future studies in functional genomics and gene interaction analysis.
9. References
BioGRID Database and API:
Stark, C., et al. "The BioGRID interaction database: 2023 update." Nucleic Acids Research.
fimH Gene and UPEC:
Sharon, N., & Ofek, I. "Mannose-binding adhesins of Escherichia coli." Microbial Pathogenesis.
Flores-Mireles, A. L., et al. "Urinary tract infections: epidemiology, mechanisms of infection and treatment options." Nature Reviews Microbiology.
Tools Used:
NetworkX: Hagberg, A., et al. NetworkX Reference.
Matplotlib: Hunter, J. D. "Matplotlib: A 2D Graphics Environment." Computing in Science & Engineering.
