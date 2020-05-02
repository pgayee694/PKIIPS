using UnityEngine;

/// <summary>
/// Script used to model an exit in our graph model.
/// </summary>
public class Exit : Node
{
    /// <summary>
    /// The default color of exit nodes.
    /// </summary>
    public override Color NodeColor { get { return Color.green; } }
}
