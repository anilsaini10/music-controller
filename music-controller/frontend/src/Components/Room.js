import React , { Component } from 'react';
import {Greed,Button, Typography, Grid} from '@material-ui/core';

import {Link} from 'react-router-dom';
import CreateRoomPage from './CreateRoomPage';
class Room extends Component {

    constructor(props) {
        super(props);
        this.state= {
            votesToSkip:2,
            guestCanPause:false,
            isHost:false,
            showSettings:false,
        };
        this.roomCode= this.props.match.params.roomCode;
        this.getRoomDetails();
        this.leaveButtonPressed =this.leaveButtonPressed.bind(this);
        this.updateShowSettings= this.updateShowSettings.bind(this);
        this.renderSettingsButton =this.renderSettingsButton.bind(this);
        this.renderSettings =this.renderSettings.bind(this);
    }

    getRoomDetails() {
        fetch("/api/get-room" + "?code=" + this.roomCode)
        .then((response)=>{
            if(!response.ok){
                this.props.leaveButtonPressed();
                this.props.history.push('/')

            }
        
        return response.json()
    })
        .then((data)=> {

            this.setState({

                votesToSkip:data.vote_to_skip,
                guestCanPause:data.guest_can_pause,
                isHost :data.is_host,

            })
        })
    }

    leaveButtonPressed() {

        const requestOptions = {
            method:"POST",
            headers:{ "Content-Type" : "application/json"},

        };
        fetch("/api/leave-room", requestOptions).then((_response)=>{
            
            this.props.leaveRoomCallback(); 
            this.props.history.push("/")

        })
    }

    updateShowSettings(value){
        this.setState({
            showSettings: value,
        })
    }

    renderSettingsButton(){
        return (
            <Grid item xs = {12} align= 'center'>

                <Button variant= 'contained' 
                color='primary' 
                onClick={() => this.updateShowSettings(true)}>
                    Settings
                </Button>

            </Grid>

        )
    }

    renderSettings() {
        return (
        <Grid container spacing={1}>

        <Grid item xs ={12} align='center'>
            <CreateRoomPage update={true}
             votesToSkip={this.state.votesToSkip}
              guestCanPause= {this.state.guestCanPause} 
              roomCode = {this.state.roomCode}
              updateCallback={() => { }}
              
              />
        </Grid>

        <Grid item xs ={12} align='center'>

            <Button variant= 'contained'
            color='secondary'
            onClick={()=> this.updateShowSettings(false)} >
                Close
                
            </Button>                 

        </Grid>

        </Grid>
        )

    }

    render() {
        if(this.state.showSettings){
            return this.renderSettings();
        }
        return (
            <Grid container spacing={1}>

                <Grid item xs={12} align="center">
                    <Typography variant='h4' component="center">
                        Code: {this.roomCode}
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                <Typography variant='h6' component="center">
                Votes: {this.state.votesToSkip}
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                <Typography variant='h6' component="center">
                Guest Can Pause: {this.state.guestCanPause.toString()}
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                <Typography variant='h6' component="center">
                   Host: {this.state.isHost.toString()}
                    </Typography>
                </Grid>

                {this.state.isHost ? this.renderSettingsButton(): null}
               
                <Grid item xs={12} align="center">
                <Button onClick={this.leaveButtonPressed} variant="contained" color="secondary" to="/" component={Link}>Leave Room</Button>
                </Grid>

            </Grid>
            // <div> 
            //     <h3>{this.roomCode}</h3>
            //     <p>Votes: {this.state.votesToSkip}</p>
            //     <p>Guest Can Pause: {this.state.guestCanPause.toString()}</p>
            //     <p>Host: {this.state.isHost.toString()}</p>
            // </div>
        )
    }


}

export default Room;

