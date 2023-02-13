import React from 'react'
import { Oval } from "react-loader-spinner";

function Loading() {
  return (
    <div>        
    <Oval
    height={60}
    width={60}
    color="#aaaaaa"
    wrapperStyle={{}}
    wrapperClass=""
    visible={true}
    ariaLabel="oval-loading"
    secondaryColor="#cccccc"
    strokeWidth={4}
    strokeWidthSecondary={4}
    />
  </div>
  )
}

export default Loading