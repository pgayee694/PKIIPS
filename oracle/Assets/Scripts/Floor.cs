using UnityEngine;

/// <summary>
/// Script to be placed onto a game object that contains
/// <code>Node</code>s as children.
/// <see cref="Node"/>
/// </summary>
public class Floor : MonoBehaviour
{
    /// <summary>
    /// The collection of nodes that belong to the floor.
    /// </summary>
    private GraphComponent[] graphComponents;

    /// <summary>
    /// Called when this game object is created.
    /// </summary>
    void Start()
    {
        graphComponents = GetComponentsInChildren<GraphComponent>();
    }

    /// <summary>
    /// Called when this game object is destroyed.
    /// Will destroy all children <code>GraphComponent</code>s.
    /// <see cref="GraphComponent"/>
    /// </summary>
    void OnDestroy()
    {
        foreach (var node in graphComponents)
        {
            Destroy(node);
        }

        Destroy(gameObject);
    }
}
