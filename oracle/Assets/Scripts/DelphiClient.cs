using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using SimpleJSON;

public class DelphiClient : MonoBehaviour
{
  // todo: move to config
  private readonly string BASE_URL = "localhost:5000";

  void Start()
  {
    //   todo: get all node info?
  }

  void Update()
  {
    // todo: update all node info?
    // note: http://answers.unity.com/answers/237847/view.html
  }

  //test methods
  public void TestGetStatuses()
  {
    StartCoroutine(CallGetStatuses(new int[] { 123, 321 }));
  }

  public void TestGetCounts()
  {
    StartCoroutine(CallGetCounts(new int[] { 123, 321 }));
  }

  public void TestUpdateStatus()
  {
    StartCoroutine(CallUpdateStatus(123, "True"));
  }

  //expected client methods
  public void GetStatuses(int[] roomIds)
  {
    StartCoroutine(CallGetStatuses(roomIds));
  }

  public void GetCounts(int[] roomIds)
  {
    StartCoroutine(CallGetCounts(roomIds));
  }

  public void UpdateStatus(int id, string status)
  {
    StartCoroutine(CallUpdateStatus(id, status));
  }

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

  //client logic
  IEnumerator CallGetStatuses(int[] roomIds)
  {
    UnityWebRequest www = UnityWebRequest.Get(BASE_URL + "/get-statuses" + GenerateParams("room_id", roomIds));
    yield return www.SendWebRequest();

    if (www.isNetworkError || www.isHttpError)
    {
      Debug.LogError(www.error);
      yield break;
    }

    JSONNode response = JSON.Parse(www.downloadHandler.text);
    print(response);

    // todo: push status into local object
    // ex: local256.status = response[256]
  }

  IEnumerator CallGetCounts(int[] roomIds)
  {
    UnityWebRequest www = UnityWebRequest.Get(BASE_URL + "/get-counts" + GenerateParams("room_id", roomIds));
    yield return www.SendWebRequest();

    if (www.isNetworkError || www.isHttpError)
    {
      Debug.LogError(www.error);
      yield break;
    }

    JSONNode response = JSON.Parse(www.downloadHandler.text);
    print(response);

    // todo: push status into local object
    // ex: local256.count = response[256]
  }

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

