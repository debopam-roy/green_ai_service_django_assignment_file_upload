import { configureStore } from '@reduxjs/toolkit';
import authenticationSlice from '../features/authentication/authenticationSlices'; // Ensure you are importing the reducer

// Function to load state from localStorage
const loadStateFromLocalStorage = () => {
    try {
        const serializedState = localStorage.getItem('userAuthentication');
        if (serializedState === null) return undefined; // No saved state found
        return JSON.parse(serializedState); // Return the parsed state
    } catch (err) {
        console.error('Could not load state from localStorage', err);
        return undefined;
    }
};

// Function to save state to localStorage
const saveState = (state) => {
    try {
        const serializedState = JSON.stringify(state);
        localStorage.setItem('userAuthentication', serializedState);
    } catch (err) {
        console.error('Could not save state', err);
    }
};

const preloadedState = loadStateFromLocalStorage() || {
    userAuthentication: {
        user_id: null,
        fullname: null,
        username: null,
        email: null,
        token: null,
        is_authenticated: false,
    },
};

export const store = configureStore({
    reducer: {
        userAuthentication: authenticationSlice,
    },
    preloadedState,
});

// Subscribe to store updates to save state to localStorage
store.subscribe(() => {
    saveState(store.getState().userAuthentication);
});
