//
//  server.swift
//  UI Tests
//
//  Created by Nayak Dheeraj on 10/08/18.
//  Copyright © 2018 Nineteen68. All rights reserved.
//
import XCTest
import Foundation
import SwiftyJSON
import SwiftSocket
import UIKit

func server(ip : String) -> (TCPServer) {

    //start server

    let server_ = TCPServer(address: ip, port: 8022)
    server_.listen()
    return server_
    
    
}
