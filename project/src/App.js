import React, { Component } from "react";
import logo from "./logo.svg";
import "./App.css";
import { Map, InfoWindow, Marker, GoogleApiWrapper } from "google-maps-react";

class App extends Component {
  fetchPlaces(mapProps, map) {
    const { google } = mapProps;
    const service = new google.maps.places.PlacesService(map);
  }
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Google Maps with React.js</h1>
        </header>
        <Map
          google={this.props.google}
          zoom={14}
          const
          style={{
            width: "70%",
            height: "100%",
            align: "center",
          }}
          onReady={this.fetchPlaces}
          visible={true}
        >
          <Marker onClick={this.onMarkerClick} name={"Current location"} />
          <InfoWindow onClose={this.onInfoWindowClose}>
            <div>
              <h1>default</h1>
            </div>
          </InfoWindow>
          {/* <Listing places={this.state.places} /> */}
        </Map>
      </div>
    );
  }
}

export default GoogleApiWrapper({
  apiKey: "AIzaSyC6yyJ9x2QijsBFpyB2N0YMK_LszR9OLl4",
})(App);
