"""
utility functions for the workshop.
"""

def visualize_docked_poses(protein_file, 
                             pose_file, 
                             cognate_file=None, 
                             animate=True,
                             cognate_color=None,
                             pose_color=None):
    """
    Creates a 3D visualization of a protein with multiple ligand poses from a single SDF file.

    Parameters:
    -----------
    protein_file : str
        Path to the protein PDB file to visualize
    pose_file : str
        Path to the SDF file containing multiple ligand poses
    cognate_file : str, optional
        Path to the cognate (static structure) file if available
    animate : bool, optional
        Whether to animate through the poses (default: True)
    cognate_color: str, optional
        Color for cognate. Default is yellow.
    pose_color: str, optional
        Color for ligand poses. Default is green.

    Returns:
    --------
    py3Dmol.view
        The 3D visualization view object
    """
    import py3Dmol

    # Get colors
    if cognate_color is None:
      cognate_color = "yellow"
    if pose_color is None:
      pose_color = "green"

    # Create the viewer
    v = py3Dmol.view()

    # Add protein structure
    with open(protein_file) as f:
        v.addModel(f.read())

    # Set protein style
    v.setStyle({'cartoon': {}, 'stick': {'radius': 0.1}})

    # Add cognate ligand if provided
    if cognate_file:
        with open(cognate_file) as f:
            v.addModel(f.read())
        v.setStyle({'model': 1}, {'stick': {'colorscheme': f'{cognate_color}Carbon', 'radius': 0.25}})

    # Add all poses from the SDF file
    model_offset = 1 if cognate_file else 0
    with open(pose_file) as f:
        pose_content = f.read()

    if animate:
        # Add all poses as animation frames
        v.addModelsAsFrames(pose_content)
        v.setStyle({'model': model_offset + 1}, {'stick': {'colorscheme': f'{pose_color}Carbon'}})
        v.animate({'interval': 1000})
    else:
        # Add as separate models
        v.addModel(pose_content)
        v.setStyle({'model': model_offset + 1}, {'stick': {'colorscheme': f'{pose_color}Carbon'}})

    # Set view
    zoom_model = 1 if cognate_file else 0
    v.zoomTo({'model': zoom_model})
    v.rotate(270)

    return v
