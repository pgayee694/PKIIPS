using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using SimpleJSON;

public class DelphiClient : MonoBehaviour
{
  //   todo: remove
  //   private readonly string EX_GET_REQUEST_URL = "https://dog.ceo/api/breed/akita/images/random";
  //   private readonly string EX_POST_REQUEST_URL = "https://reqres.in/api/users";

  // todo: update w/ actual url
  private readonly string GET_NODES_URL = "";
  private readonly string DISABLE_NODE_URL = "";

  void Start()
  {
    //   todo: get all node info?
  }

  void Update()
  {
    // todo: update all node info?
    // note: http://answers.unity.com/answers/237847/view.html
  }

  public void TestGetNodes()
  {
    StartCoroutine(GetNodes());
  }

  public void TestDisableNode(string id)
  {
    StartCoroutine(DisableNode(id));
  }

  IEnumerator GetNodes()
  {
    UnityWebRequest www = UnityWebRequest.Get(GET_NODES_URL);
    yield return www.SendWebRequest();

    if (www.isNetworkError || www.isHttpError)
    {
      Debug.LogError(www.error);
      yield break;
    }

    JSONNode response = JSON.Parse(www.downloadHandler.text);

    // todo: update local node info
  }

  IEnumerator DisableNode(string id)
  {
    Dictionary<string, string> requestBody = new Dictionary<string, string>();
    requestBody.Add("id", id);

    UnityWebRequest www = UnityWebRequest.Post(DISABLE_NODE_URL, requestBody);
    yield return www.SendWebRequest();

    if (www.isNetworkError || www.isHttpError)
    {
      Debug.LogError(www.error);
      yield break;
    }

    JSONNode response = JSON.Parse(www.downloadHandler.text);

    // todo: disable local node
  }
}
