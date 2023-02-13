import React, { useState} from "react";
import Loading from "./Loading";
import { getVideoFiles, pathAPI, uploadForm } from "../../utils/pathAPI";
import "./UploadFile.css";
import notebook from "../../assets/image/notebook.png";
import playButton from "../../assets/image/button.png";

function UploadFile() {
  const [fileName, setFileName] = useState('');
  const [loading, setLoading] = useState(undefined);
  const [videos, setVideos] = useState([]);
  const [videoPlay, setVideoPlay] = useState(undefined);
  const [downloadLink, setDownloadLink] = useState('/');
  let fileReader = new FileReader();

  fileReader.onload = (e) => {
    console.log('video onload');
    const previewImage = String(e.target?.result);
    setVideoPlay(previewImage);
    setDownloadLink(previewImage);
  }

  async function submitForm(e) {
    const formData = new FormData();

    formData.append("file", e.target.files[0]);
    setFileName(e.target.value);
    setLoading(true);
    await getVideo(formData);
  }

  async function getVideo (formData) {
    const res = await uploadForm(formData);
    if (res.status === 200) {
      const {data} = await pathAPI();
      const files = await getVideoFiles(data, formData);
      setVideos(files);
      setLoading(false);
    }
  }

  function clickPlayButton(e) {
    switch(e.target.id) {
      case 'button1':
        console.log('click button1');
        fileReader.readAsDataURL(videos[0]);
        break;
      case 'button2':
        console.log('click button2');
        fileReader.readAsDataURL(videos[1]);
        break;
      case 'button3':
        console.log('click button3');
        fileReader.readAsDataURL(videos[2]);
        break;
      case 'button4':
        console.log('click button4');
        fileReader.readAsDataURL(videos[3]);
        break;
      default:
        // no default
        break;
    }
  }

  // * components
  const FileForm = () => {
    return (
      <form
        action="#"
        id="file-form"
        onSubmit={(e) => {
          e.preventDefault();
        }}
      >
        <input
          type="text"
          id="show-input"
          value={fileName}
          name="url"
          placeholder="첨부파일"
          readOnly
        />
        <label htmlFor="file-input"></label>
        <input
          type="file"
          id="file-input"
          accept="video/*"
          onChange={(e) => submitForm(e)}
        />
      </form>
    );
  };

  const ShowLoading = () => {
    if (loading === undefined) {
      return <div>동영상 url을 입력하거나, 파일을 업로드 하세요.</div>;
    }

    if (loading === true) {
      return <Loading />;
    }

    return (
      <>
        <div className="play-button-container">
          <img
            className="play-button"
            id="button1"
            src={playButton}
            alt="플레이 버튼1"
            onClick={(e) => clickPlayButton(e)}
          />
          <img
            className="play-button"
            id="button2"
            src={playButton}
            alt="플레이 버튼2"
            onClick={(e) => clickPlayButton(e)}
          />
          <img
            className="play-button"
            id="button3"
            src={playButton}
            alt="플레이 버튼3"
            onClick={(e) => clickPlayButton(e)}
          />
          <img
            className="play-button"
            id="button4"
            src={playButton}
            alt="플레이 버튼4"
            onClick={(e) => clickPlayButton(e)}
          />
        </div>
        <div id="download-container">
          <a href={downloadLink} download={downloadLink ? true : alert('동영상을 선택해주세요.')}>Download</a>
        </div>
      </>
    );
  };

  const VideoPlayer = () => {
    return (
      <video id='video' controls={videoPlay ? 'controls' : ''}>
        <source src={videoPlay} type="video/mp4" />
      </video>
    )
  }

  return (
    <section id="input-section">
      <div id="input-music-container">
        <div className="content-area-container">
          <nav>
            <span id="upload">Upload</span>
          </nav>
          <FileForm />
          <p id="input-info">
            업로드한 영상의 최대 15분까지 음성인식이 가능하고, 생성되는 음원은
            최대 1분 20초까지 생성됩니다.
          </p>
        </div>
      </div>
      <img src={notebook} alt="노트북 이미지" />
      <VideoPlayer />
      <div id="load-music-container">
        <div className="content-area-container">
          <ShowLoading />
        </div>
      </div>
    </section>
  );
}

export default UploadFile;
