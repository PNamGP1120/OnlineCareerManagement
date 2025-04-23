import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import React from "react";
import {Provider as PaperProvider} from 'react-native-paper'
import LoginScreen from './components/Screen/LoginScreen'

export default function App() {
  return (
    <PaperProvider>
      <LoginScreen/>
    </PaperProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
