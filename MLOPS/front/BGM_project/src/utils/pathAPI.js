import axios from "axios";

const UPLOAD_URL = [
  "http://STS,SC/upload",
  "http://RF1/upload",
  "http://RF2/upload",
  "http://RF3/upload",
  "http://RF4/upload",
];

const PATH_URL = [
  "http://RF1/file/",
  "http://RF2/file/",
  "http://RF3/file/",
  "http://RF4/file/",
];

const postUploadAPI = async (url, formData) => {
  try {
    const res = await axios(url, {
      method: "POST",
      data: formData,
      headers: {
        "Content-Type": "multipart/form-data",
      },
      responseType: "arraybuffer",
    });
  
    return res;
  } catch(e) {
    console.log(e);
  } 
};

const getVideoAPI = async (url, formData) => {
  try {
    const res = await axios(url, {
      method: "GET",
      data: formData,
      headers: {
        "Content-Type": "multipart/form-data",
      },
      responseType: "arraybuffer",
    });
  
    return res;
  } catch (e) {
    console.log(e);
  }
};

export const uploadForm = async (formData) => {
  const res = postUploadAPI(UPLOAD_URL[0], formData).then(
    postUploadAPI(UPLOAD_URL[1], formData).then(
      postUploadAPI(UPLOAD_URL[2], formData).then(
        postUploadAPI(UPLOAD_URL[3], formData).then(
          postUploadAPI(UPLOAD_URL[4], formData).then()
        )
      )
    )
  )

  return res;
};

export const pathAPI = async () => {
  try {
    const res = axios.get("http://Local K8s/signal");
    return res;
  } catch (e) {
    console.log(e);
    throw new Error(e);
  }
};

const makeVideoFile = (res) => {
  const file = new File([res.data], "videoFile");
  return file;
};

export const getVideoFiles = async (path, formData) => {
  const files = [];

  const file1 = await getVideoAPI(PATH_URL[0] + path, formData);
  files.push(makeVideoFile(file1));
  const file2 = await getVideoAPI(PATH_URL[1] + path, formData);
  files.push(makeVideoFile(file2));
  const file3 = await getVideoAPI(PATH_URL[2] + path, formData);
  files.push(makeVideoFile(file3));
  const file4 = await getVideoAPI(PATH_URL[3] + path, formData);
  files.push(makeVideoFile(file4));

  return files;
};
