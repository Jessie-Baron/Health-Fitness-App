import React, { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Redirect, useHistory } from "react-router-dom";
import * as runActions from "../store/runs";
import './runs.css'

const RunDropdown = () => {

    const user = useSelector((state) => state.session.user);
    const runs = Object.values(useSelector((state) => state.runs));
    const dispatch = useDispatch()
    const history = useHistory()
    const [hasSubmitted, setHasSubmitted] = useState(false);
    const [show, setShow] = useState("");
    const [date, setDate] = useState("")
    const [distance, setDistance] = useState("")
    const [duration, setDuration] = useState("")
    const [validationErrors, setValidationErrors] = useState([]);

    const selectShow = (value) => {
        console.log(value)
        setShow(value)
    }

    useEffect(() => {
        dispatch(runActions.fetchAllRuns());
        dispatch(runActions.fetchAllUsers())
    }, [dispatch]);


    useEffect(() => {
        dispatch(runActions.fetchAllRuns());
    }, [dispatch]);

    const handleSubmit = async (e) => {
        // Prevent the default form behavior so the page doesn't reload.
        e.preventDefault();
        setHasSubmitted(true);

        // Create a new object for the song form information.
        console.log("this is the show >>>>>>>>>>>", show)
        const runForm = {
            "duration": duration,
            "date": date,
            "distance": distance
        };

        await dispatch(runActions.fetchPostRuns(runForm))
        user.runs.push(runForm)
        await dispatch(runActions.fetchAllUsers())
        await dispatch(runActions.fetchAllRuns())
        .then(history.push("/"))



        // Reset the form state.
        setValidationErrors([]);
        setHasSubmitted(false);
    }

    return (
        <div class='dropdown-container'>
            <div class='dropdown'>
                <form onSubmit={handleSubmit}>
                    <ul>
                        {validationErrors.map((error, idx) => (
                            <li key={idx}>{error}</li>
                        ))}
                    </ul>
                    <div class='dropdown-text'>
                        <h3>Hello, {user?.username}</h3>
                        <h5>Please input run data to track</h5>
                    </div>
                    <label>Select the Date of the run</label>
                    <input
                        class='select-2'
                        onChange={(e) => setDate(e.target.value)}
                        type='date'
                    >
                    </input>
                    <label>How far did you run?</label>
                    <input
                        class='select'
                        onChange={(e) => setDistance(e.target.value)}
                    ></input>
                    <label>Have long did you run?</label>
                    <input
                        class='select'
                        onChange={(e) => setDuration(e.target.value)}
                    >
                    </input>
                    <button
                        type='submit'
                    >
                        Add
                    </button>
                </form>
            </div>
        </div>
    )
}

export default RunDropdown;
