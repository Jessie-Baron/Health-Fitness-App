import React, { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Redirect, useHistory } from "react-router-dom";
import * as runsActions from "../store/runs";
import './runs.css'

const RunsGrid = () => {

    const user = useSelector((state) => state.session.user);
    const runs = Object.values(useSelector((state) => state.runs));
    const dispatch = useDispatch()
    const history = useHistory()

    console.log(runs)


    useEffect(() => {
        dispatch(runsActions.fetchAllRuns());
        dispatch(runsActions.fetchAllUsers())
    }, [dispatch]);

    const deleteRun = async (run) => {
        let idx = user.runs.findIndex((ele) => ele.title === run.title)
        user.runs.splice(idx, 1)
        await dispatch(runsActions.fetchAllUsers())
        await dispatch(runsActions.fetchAllRuns())
    };

    return (
        <div class='runs-grid'>
            {user.runs?.map((run) => (
                <div class='grid-item'>
                    <div>{run?.date}</div>
                    <div>{run?.distance}</div>
                    <div>{run?.duration}</div>
                    <button onClick={() => deleteRun(run)}>DELETE</button>
                    <button onClick={() => deleteRun(run)}>EDIT</button>
                </div>
            ))}
        </div>
    )
}

export default RunsGrid;
