using UnityEngine;

/// <summary>
/// Script to be placed onto a game object that contains
/// <code>Node</code>s as children.
/// <see cref="Node"/>
/// </summary>
public class Floor : MonoBehaviour
{
    /// <summary>
    /// Sets the delay at which the UpdateRooms is called in seconds.
    /// </summary>
    private static float DELAY_UPDATE_TIME = 0.0f;

    /// <summary>
    /// Sets the interval at which the UpdateRooms is called in seconds.
    /// </summary>
    private static float UPDATE_INTERVAL_TIME = 0.5f;

    /// <summary>
    /// The collection of rooms that belong to the floor.
    /// </summary>
    private Room[] rooms;


    /// <summary>
    /// Called when this game object is created.
    /// </summary>
    void Start()
    {
        rooms = GetComponentsInChildren<Room>();
        InvokeRepeating("UpdateRooms", DELAY_UPDATE_TIME, UPDATE_INTERVAL_TIME);
    }

    /// <summary>
    /// Called when this game object is destroyed.
    /// Will destroy all children <code>Node</code>s.
    /// <see cref="Node"/>
    /// </summary>
    void OnDestroy()
    {
        foreach (var node in GetComponentsInChildren<GraphComponent>())
        {
            Destroy(node);
        }

        Destroy(gameObject);
    }


    /// <summary>
    /// Continiously called to update the rooms of the floor.
    /// Updates according to the value of the <code>UPDATE_INTERVAL_TIME</code> property.
    /// <see cref="UPDATE_INTERVAL_TIME"/>
    /// </summary>
    void UpdateRooms()
    {
        if (rooms.Length > 0)
        {
            DelphiClient.Instance.UpdateRooms(rooms);
        }
    }
}
