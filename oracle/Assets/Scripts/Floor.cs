using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Floor : MonoBehaviour
{
    void OnDestroy()
    {
        foreach(var node in GetComponentsInChildren<Node>())
        {
            Destroy(node);
        }

        Destroy(gameObject);
    }
}
