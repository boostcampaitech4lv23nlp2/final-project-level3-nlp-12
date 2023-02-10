import axios from "axios";

const UPLOAD_URL = [
  "http://101.101.209.53:30001/upload",
  "http://118.67.133.154:30002/upload",
  "http://27.96.134.124:30002/upload",
  "http://118.67.142.47:30002/upload",
  "http://118.67.133.198:30002/upload",
];

const PATH_URL = [
  "http://118.67.133.154:30002/file/",
  "http://27.96.134.124:30002/file/",
  "http://118.67.142.47:30002/file/",
  "http://118.67.133.198:30002/file/",
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
    const res = axios.get("http://219.255.27.88:8383/signal");
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
