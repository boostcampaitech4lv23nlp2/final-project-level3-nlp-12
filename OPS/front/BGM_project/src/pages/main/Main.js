import React from 'react'
import Header from '../../components/Header'
import Footer from '../../components/Footer'
import PageInfo from './PageInfo'
import UploadFile from './UploadFile'

function Main() {
  return (
    <>
      <Header />
      <main>
        <PageInfo />
        <UploadFile />
      </main>
      <Footer />
    </>
  )
}

export default Main
