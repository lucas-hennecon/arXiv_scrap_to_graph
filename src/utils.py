def convert_metadata_for_neo4j(metadata):
    """
    Convert metadata from arXiv to a format suitable for Neo4j.
    """
    return {
        "title": metadata["title"],
        "authors": metadata["authors"],
        "publication_year": int(metadata["publication_date"].split("-")[0]),
        "paper_index": metadata["link"].split("/")[-1],
    }


if __name__ == "__main__":
    metadata = {
        "title": "Physics-guided Neural Networks (PGNN): An Application in Lake\n  Temperature Modeling",
        "authors": [
            "Arka Daw",
            "Anuj Karpatne",
            "William Watkins",
            "Jordan Read",
            "Vipin Kumar",
        ],
        "publication_date": "2017-10-31T12:24:26Z",
        "summary": "This paper introduces a framework for combining scientific knowledge of\nphysics-based models with neural networks to advance scientific discovery. This\nframework, termed physics-guided neural networks (PGNN), leverages the output\nof physics-based model simulations along with observational features in a\nhybrid modeling setup to generate predictions using a neural network\narchitecture. Further, this framework uses physics-based loss functions in the\nlearning objective of neural networks to ensure that the model predictions not\nonly show lower errors on the training set but are also scientifically\nconsistent with the known physics on the unlabeled set. We illustrate the\neffectiveness of PGNN for the problem of lake temperature modeling, where\nphysical relationships between the temperature, density, and depth of water are\nused to design a physics-based loss function. By using scientific knowledge to\nguide the construction and learning of neural networks, we are able to show\nthat the proposed framework ensures better generalizability as well as\nscientific consistency of results. All the code and datasets used in this study\nhave been made available on this link \\url{https://github.com/arkadaw9/PGNN}.",
        "link": "http://arxiv.org/abs/1710.11431v3",
    }
    print(convert_metadata_for_neo4j(metadata))
