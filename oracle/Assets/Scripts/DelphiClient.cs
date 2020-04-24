using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using System.Linq;
using SimpleJSON;

/// <summary>
/// Client used to communicate with Delphi.
/// </summary>
public class DelphiClient : MonoBehaviour
{
    /// <summary>
    /// Base URL of all of Delphi's endpoints.
    /// </summary>
    private static readonly string BASE_URL = Config.cfg["delphi client"]["base-url"].StringValue;

    /// <summary>
    /// Single instance of the client.
    /// </summary>
    private static DelphiClient _instance;

    /// <summary>
    /// Publicly accessible client instance.
    /// </summary>
    public static DelphiClient Instance
    {
        get
        {
            if (_instance == null)
                _instance = new GameObject("DelphiClient").AddComponent<DelphiClient>();
            return _instance;
        }
    }


    /// <summary>
    /// Prevents the client from being destroyed on scene change.
    /// </summary>
    void Awake()
    {
        if (_instance != null) Destroy(this);
        DontDestroyOnLoad(this);
    }


    /// <summary>
    /// Updates all of the fields for each of the rooms supplied.
    /// </summary>
    public void UpdateRooms(Room[] rooms)
    {
        int[] roomIds = rooms.Select(room => room.Id).ToArray();
        StartCoroutine(CallGetCounts(roomIds, (response) => rooms.ToList().ForEach(room => room.PeopleCount = response[room.Id])));
        // todo: update room status
    }


    /// <summary>
    /// Helper method used to generate a list of parameters.
    /// </summary>
    private string GenerateParams(string key, int[] values)
    {
        return "?" + string.Join("&", values.Select(value => key + "=" + value).ToArray());
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