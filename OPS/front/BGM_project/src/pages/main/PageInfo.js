import React from 'react'
import './PageInfo.css'

function PageInfo() {
  return (
    <section id="info-section">
      <div id="devide">
        <div className="devide-line"></div>
        <div id="devide-center">what we do</div>
        <div className="devide-line"></div>
      </div>
      <div id="info-section-item">
        <h1>콘텐츠 맞춤형 BGM 생성</h1>
        <p>영상의 음성데이터 감성분석을 통해 맞춤형 BGM을 만드는 프로젝트입니다.</p>
      </div>
    </section>
  )
}

export default PageInfo
