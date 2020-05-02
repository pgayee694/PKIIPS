using UnityEngine;

/// <summary>
/// Script used to model a hallway in our graph model.
/// </summary>
public class Hallway : Node
{
    /// <summary>
    /// The default color of hallway nodes.
    /// </summary>
    public override Color NodeColor { get { return Color.red; } }
}
