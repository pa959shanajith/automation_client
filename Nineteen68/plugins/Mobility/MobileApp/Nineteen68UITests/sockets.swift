//
//  sockets.swift
//  UI Tests
//
//  Created by Nayak Dheeraj on 08/08/18.
//  Copyright © 2018 Nineteen68. All rights reserved.
//

import Foundation
import SwiftSocket
import XCTest
import SwiftyJSON
class sock{
    
    func echoService(client: TCPClient,type : String)-> (Any){
        
        func bundle_id() -> (String){
            print("bundle_id")
            
            
            
            var data = client.read(2)
            var strnum = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
            let num=strnum!
            let exampeStruct = Int(num.intValue)
            
            
            //READ STR
            data = client.read(exampeStruct)
            var str = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
           
            
            //send dict ->  .json -> string
            var dict : [String:String] = ["hello":"human"]
            var jsonObj = JSON(dict)
            let string = jsonObj.rawString()
            let lol = string?.data(using: .utf8)
            var msg = client.send(data:lol!)
            return str! as String
            }
        
        print("Newclient from:\(client.address)[\(client.port)]")
        switch type {
        case "bundle_id":
            return bundle_id()
            
        default:
            return "error"
        }

        //client.send(data: d!)
        //client.close()

    }

    
    func testServer(type:String) -> (Any) {
        let server = TCPServer(address: "10.60.72.52", port: 8022)
        switch server.listen() {
        case .success:
            while true {
                if var client = server.accept() {
                    return echoService(client: client, type: type)
                } else {
                    return("accept error")
                }
            }
        case .failure(let error):
            return (error)
            
        }
        
        return "done"

   }

}






















/*
 
 XCUIApplication(bundleIdentifier: "com.apple.mobilecal").launch()
 let button = XCUIApplication(bundleIdentifier: "com.apple.mobilecal").buttons["Add"]
 let frame = button.frame
 let xPosition = frame.origin.x
 let yPosition = frame.origin.y
 let height = app.buttons.element.frame.size.height
 let width = app.buttons.element.frame.size.width
 let x = app.buttons.element.frame.origin.x
 let y = app.buttons.element.frame.origin.y
 print(xPosition,yPosition)
 
 
 
 gettting the cordinates
 check assertion
 XCTAssert(app.staticTexts["Welcome"].exists)
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 func echoService(client: TCPClient) {
 
 
 func convertstr(data:[Byte])->(String){
 var str = String(bytes: data, encoding: String.Encoding.utf8)
 return str!
 
 }
 
 func input()->(String){
 print("input")
 var len = 2
 var data = client.read(len)
 var variable = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
 len = (variable?.integerValue)!
 print(len)
 var input = client.read(len)
 print("read")
 var str = NSString(bytes: input!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
 print(str)
 return str as! (String)
 }
 
 func keyword(){
 print("keyword")
 var data = client.read(2)
 var strnum = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
 let num=strnum!
 let exampeStruct = Int(num.intValue)
 print(exampeStruct)
 data = client.read(exampeStruct)
 var str = NSString(bytes: data!, length: data!.count, encoding: String.Encoding.utf8.rawValue)
 print(str!)
 switch str {
 case "openb": return web().openbrowser()
 
 case "navig": return web().navigate(input: input())
 default: print("no match found")
 
 }
 
 }
 
 
 print("Newclient from:\(client.address)[\(client.port)]")
 keyword()
 
 
 
 
 let lol = "greetings humans".data(using: .utf8)
 var msg = client.send(data:lol!)
 print("done")
 
 //client.send(data: d!)
 //client.close()
 
 }
 
 
 func testServer() {
 let server = TCPServer(address: "10.60.72.52", port: 8022)
 switch server.listen() {
 case .success:
 while true {
 if var client = server.accept() {
 echoService(client: client)
 } else {
 print("accept error")
 }
 }
 case .failure(let error):
 print(error)
 
 }
 
 }
 
 }
*/
