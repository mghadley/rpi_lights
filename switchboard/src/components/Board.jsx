import React, { Component } from 'react';
import 'rpio';

class Board extends Component {
	constructor(props) {
		super(props)
    this.state = { light: false }
    this.toggleLight = this.toggleLight.bind(this)
	}

  toggleLight() {
    let light = !this.state.light;
    this.setState({ light });
    this.sendStatus();
  }

  sendStatus() {
    if(this.state.light) {
      rpio.write(18, rpio.HIGH);
    } else {
      rpio.wirte(18, rpio.LOW);
    }
  }

	render() {
		return(
			<h1 onClick={this.toggleLight}>{this.state.light.toString()}</h1>
		)
	}
}

export default Board;
