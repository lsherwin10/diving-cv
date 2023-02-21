//
//  Pose_Estimation_DiverApp.swift
//  Pose Estimation Diver
//
//  Created by Logan Sherwin on 9/1/22.
//

import SwiftUI

@main
struct Pose_Estimation_DiverApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(ViewModel())
                .onAppear {
                    UserDefaults.standard.setValue(false, forKey: "_UIConstraintBasedLayoutLogUnsatisfiable")
                }
//            RecordingView()
        }
    }
}
