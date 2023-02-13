import React from 'react'
import './Header.css'

function Header() {
  return (
    <header>
      <nav>
        <div id="nav-icon">Team.ET</div>
        <div id="nav-nav">
          <a href="/"><span>Home</span></a>
          <a href="/"><span>About</span></a>
          <a href="/"><span>Github</span></a>
          <a href="/"><span>E-mail</span></a>
        </div>
      </nav>
      <div id="header-explain">
        <h1>ET</h1>
        <p>This page is final project result team with E.T</p>
      </div>
    </header>
  )
}

export default Header
