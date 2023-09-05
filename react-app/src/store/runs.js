const POST_RUNS = "Runs/POST_RUNS";
const EDIT_RUNS = "Runs/EDIT_RUNS";
const GET_RUNS = "Runs/GET_RUNS";
const DELETE_RUNS = "Runs/DELETE_RUNS"

const postRuns = (Runs) => ({
  type: POST_RUNS,
  payload: Runs,
});

const editRuns = (Runs) => ({
  type: EDIT_RUNS,
  payload: Runs
});

const getRuns = (Runs) => ({
  type: GET_RUNS,
  payload: Runs,
});

const deleteRuns= (id) => ({
  type: DELETE_RUNS,
  payload: id
});

export const fetchAllRuns = () => async (dispatch) => {
  const response = await fetch("/api/runs");
  if (response.ok) {
    const runs = await response.json();
    dispatch(getRuns(runs));
    return runs;
  }
};

export const fetchAllUsers = () => async (dispatch) => {
  const response = await fetch("/api/users");
  if (response.ok) {
    const Runs = await response.json();
    dispatch(getRuns(Runs));
    return Runs;
  }
};

export const fetchPostRuns = (runs) => async (dispatch) => {
  console.log("This is the data >>>>>>>>>>>", runs)
  const response = await fetch(`/api/runs`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(runs),
  });
  if (response.ok) {
    const Runs = await response.json();
    dispatch(postRuns(Runs));
    return response;
  }
};

export const fetchEditRuns = (RunsId, payload) => async (dispatch) => {
  console.log(RunsId)
  // const formData = new FormData();
  // formData.append("title", newTitle);
  // formData.append("body", newBody);
  const res = await fetch(`/api/Runs/${RunsId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });
  if (res.ok) {
    const data = await res.json()
    dispatch(editRuns(data))
    return data
  }
}

export const fetchDeleteRuns = (id, showId) => async (dispatch) => {
  const response = await fetch(`/api/user/${id}/${showId}`, {
    method: "DELETE",
  });
  console.log(response)
  if (response.ok) {
    dispatch(deleteRuns(id))
    return response
  }
}

const initialState = {};

export default function reducer(state = initialState, action) {
  let newState;
  switch (action.type) {
    case GET_RUNS:
      newState = action.payload;
      return newState;
    case POST_RUNS:
      newState = Object.assign({}, state);
      newState[action.payload.id] = action.payload;
      return newState;
    case EDIT_RUNS:
      newState = Object.assign({}, state);
      newState[action.payload.id] = action.payload;
      return newState;
    case DELETE_RUNS:
      newState = Object.assign({}, state);
      delete newState[action.payload.id];
      return newState;
    default:
      return state;
  }
}
