using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Script to be placed onto a game object that contains
/// <code>Node</code>s as children.
/// <see cref="Node"/>
/// </summary>
public class Floor : MonoBehaviour
{

  public DelphiClient client;

  void Start()
  {
    InvokeRepeating("UpdateRooms", 0.0f, 5.0f);
  }

  void UpdateRooms()
  {
    foreach (var room in GetComponentsInChildren<Room>())
    {
      client.UpdateRoom(room);
    }
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
}
