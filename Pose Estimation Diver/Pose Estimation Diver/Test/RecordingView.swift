//
//  RecordingView.swift
//  Pose Estimation Diver
//
//  Created by Logan Sherwin on 9/18/22.
//

import SwiftUI

struct RecordingView: View {
    @State private var timer = 5
    @State private var onComplete = false
    @State private var recording = false
    
    var body: some View {
        ZStack {
            VideoRecordingView(timeLeft: $timer, onComplete: $onComplete, recording: $recording)
            VStack {
                Button(action: {self.recording.toggle()}, label: {
                ZStack {
                    Circle()
                        .fill(Color.white)
                        .frame(width: 65, height: 65)
                    
                    Circle()
                        .stroke(Color.white,lineWidth: 2)
                        .frame(width: 75, height: 75)
                }
                })
                Button(action: {
                    self.timer -= 1
                    print(self.timer)
                }, label: {
                    Text("Toggle timer")
                })
                .foregroundColor(.white)
                .padding()
                Button(action: {
                    self.onComplete.toggle()
                }, label: {
                    Text("Toggle completion")
                })
                .foregroundColor(.white)
                .padding()
            }
        }
    }
    
}

struct RecordingView_Previews: PreviewProvider {
    static var previews: some View {
        RecordingView()
    }
}
