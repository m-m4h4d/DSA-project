import React
 from 'react';
 import { Component } from 'react';
import {Map, InfoWindow, Marker, GoogleApiWrapper} from 'google-maps-react';
 
export class MapContainer extends Component {
  render() {
    return (
      <Map google={this.props.google} zoom={14}>
 
        <Marker onClick={this.onMarkerClick}
                name={'Current location'} />
 
        <InfoWindow onClose={this.onInfoWindowClose}>
        </InfoWindow>
      </Map>
    );
  }
}
 

export default GoogleApiWrapper({
  apiKey: "AIzaSyC6yyJ9x2QijsBFpyB2N0YMK_LszR9OLl4"
})(MapContainer);
