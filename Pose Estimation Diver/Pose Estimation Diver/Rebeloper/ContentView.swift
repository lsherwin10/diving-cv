//
//  ContentView.swift
//  Pose Estimation Diver
//
//  Created by Logan Sherwin on 9/18/22.
//

import SwiftUI
import PhotosUI
import AVKit

struct ContentView: View {
    @StateObject var mediaPickerService = MediaPickerService()
    
    var body: some View {
        VStack {
            
            if mediaPickerService.mediaPickerResult.count() == 0 {
                Image(systemName: "photo.on.rectangle.angled")
                    .font(.system(size: 200))
                    .foregroundColor(.gray)
                    .opacity(0.2)
            } else {
                mediaPickerResultView()
            }
        }
        .navigationBarTitleDisplayMode(.inline)
        .navigationTitle("Media Picker")
        .toolbar {
            ToolbarItem(placement: .cancellationAction) {
                HStack {
                    Button {
                        mediaPickerService.removeAll()
                    } label: {
                        Image(systemName: "trash")
                    }
                    .buttonStyle(.bordered)
                }
            }
            ToolbarItem(placement: .primaryAction) {
                Menu {
                    VStack {
                        Text("Camera")
                        
                        Button {
                            mediaPickerService.present(.videoFromCamera(allowsEditing: false))
                        } label: {
                            Label("Capture video from camera", systemImage: "play.rectangle")
                        }
                    }
                    
                    VStack {
                        Text("Photos Library")
                        
                        Button {
                            mediaPickerService.present(.videos(selectionLimit: .exactly(1)))
                        } label: {
                            Label("Pick video", systemImage: "play.rectangle")
                        }
                    }
                }
                
            }
            .mediaPickerSheet(service: mediaPickerService) {
                print("onCancel")
            } onDismiss: {
                print("onDismiss")
            }
            .onReceive(mediaPickerService.$videoUrls) { videoUrl in
                print("Got videoUrls: \(videoUrl.count)")
            }
            
        }
    }
    
    func mediaPickerResultView() -> some View {
        ScrollView {
            switch mediaPickerService.mediaPickerResult.type {
            case .single:
                MediaPickerSingleView(info: mediaPickerService.mediaPickerResult.info)
                    .scaledToFill()
                    .fram(maxWidth: .infinity, minHeight: 200, idealHeight: 200)
                    .clipped()
            }
        }
    }
    
    func videoUrlsView() -> some View {
        ScrollView {
            ForEach(mediaPickerService.videoUrls, id: \.self) { videoUrl in
                VideoPlayer(player: AVPlayer(url: videoUrl))
                    .scaledToFill()
                    .frame(maxWidth: .infinity, minHeight: 200, idealHeight: 200)
                    .clipped()
            }
        }
    }
    
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
