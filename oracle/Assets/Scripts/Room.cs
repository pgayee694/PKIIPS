using UnityEngine;

/// <summary>
/// Script used to model a room in our graph model.
/// </summary>
public class Room : Node
{
    /// <summary>
    /// The default color of room nodes.
    /// </summary>
    public override Color NodeColor { get { return Color.white; } }
}
