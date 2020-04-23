using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using SimpleJSON;

/// <summary>
/// Client used to make calls to and from Delphi.
/// </summary>
public class DelphiClient : MonoBehaviour
{
  // todo: move to config
  private readonly string BASE_URL = "localhost:5000";

  /// <summary>
  /// Updates all of the fields associated with a room.
  /// </summary>
  public void UpdateRoom(Room room)
  {
    StartCoroutine(CallGetCounts(new int[] { room.Id }, (response) => room.PeopleCount = response[room.Id]));
    // todo: update room status
    // StartCoroutine(CallGetStatuses(new int[] { room.Id }, (response) => room.Status = response[room.Id]));
  }

  /// <summary>
  /// Helper method used to generate a list of parameters.
  /// </summary>
  string GenerateParams(string key, int[] values)
  {
    string output = "?";
    for (int i = 0; i < values.Length; i++)
    {
      if (i != 0) output += "&";
      output += key + "=" + values[i];
    }
    return output;
  }

  /// <summary>
  /// Gets the status of all of the rooms given in the list of ids.
  /// </summary>
  IEnumerator CallGetStatuses(int[] roomIds, System.Action<JSONNode> callback)
  {
    UnityWebRequest www = UnityWebRequest.Get(BASE_URL + "/get-statuses" + GenerateParams("room_id", roomIds));
    yield return www.SendWebRequest();

    if (www.isNetworkError || www.isHttpError)
    {
      Debug.LogError(www.error);
      yield break;
    }

    JSONNode response = JSON.Parse(www.downloadHandler.text);

    callback(response);
  }

  /// <summary>
  /// Gets the people count of all of the rooms given in the list of ids.
  /// </summary>
  IEnumerator CallGetCounts(int[] roomIds, System.Action<JSONNode> callback)
  {
    UnityWebRequest www = UnityWebRequest.Get(BASE_URL + "/get-counts" + GenerateParams("room_id", roomIds));
    yield return www.SendWebRequest();

    if (www.isNetworkError || www.isHttpError)
    {
      Debug.LogError(www.error);
      yield break;
    }

    JSONNode response = JSON.Parse(www.downloadHandler.text);

    callback(response);
  }

  /// <summary>
  /// Updates the status of the room associated with the given id.
  /// </summary>
  IEnumerator CallUpdateStatus(int id, string status)
  {
    JSONObject requestData = new JSONObject();
    requestData.Add("enable", status);

    UnityWebRequest www = UnityWebRequest.Put(BASE_URL + "/enable/" + id, requestData.ToString());
    www.SetRequestHeader("Content-Type", "application/json");
    yield return www.SendWebRequest();

    if (www.isNetworkError || www.isHttpError)
    {
      Debug.LogError(www.error);
      yield break;
    }
  }
}