# P2P Chat System

## Overview
The **P2P Chat System** is a peer-to-peer messaging application that allows users to register with peers, exchange messages, and manage their network of connected peers. The application uses **ZeroMQ** to establish seamless communication between peers in a distributed manner.

This project was built as part of an assignment to design and implement a simple P2P chat system. It demonstrates the core principles of peer-to-peer architecture, including message broadcasting, peer registration, and dynamic connectivity.

---

## Features
1. **Peer Registration**:
   - Users can dynamically connect with other peers by registering their IP address and port.
   - Upon successful registration, both peers are notified of the connection.

2. **Messaging**:
   - Users can send direct messages to connected peers.
   - Messages are delivered instantly if the recipient is online.

3. **Dynamic Peer Discovery**:
   - Peers can view a list of all currently connected peers.

4. **Robust and Simple Interface**:
   - A command-line interface ensures that the application is lightweight and easy to use.

---

## Why ZeroMQ?
ZeroMQ was chosen over OpenChord and other distributed frameworks due to:
- **Ease of Use**: ZeroMQ is simpler to implement and manage, especially for a messaging-focused P2P system.
- **Scalability**: It provides high-performance asynchronous messaging, making it ideal for distributed systems.
- **Cross-Platform Compatibility**: ZeroMQ works seamlessly on multiple platforms without requiring extensive configuration.

While OpenChord aligns with structured peer-to-peer systems like Distributed Hash Tables (DHTs), its complexity and dependency issues made it less suitable within the project's timeframe.

---

## What’s Missing?
Due to time constraints, the following features were not implemented:
1. **Friend Management**:
   - Originally planned to include a friend request/approval mechanism.
   - This was excluded to focus on core P2P functionality and ensure a fully operational messaging system.

---

## Requirements
- **Python 3.10 or higher**
- **ZeroMQ** (pyzmq)

Install dependencies:
```bash
pip install -r requirements.txt
