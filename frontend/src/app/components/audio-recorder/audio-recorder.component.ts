import { Component, EventEmitter, Output, Input, NgZone } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-audio-recorder',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './audio-recorder.component.html',
    styleUrl: './audio-recorder.component.css'
})
export class AudioRecorderComponent {
    @Output() audioRecorded = new EventEmitter<Blob>();
    @Output() listenRequested = new EventEmitter<void>();
    @Output() pauseRequested = new EventEmitter<void>();
    @Output() resumeRequested = new EventEmitter<void>();
    @Output() recordingStateChanged = new EventEmitter<boolean>();
    @Input() audioUrl: string | null = null;
    @Input() isPlaying = false;
    @Input() isPaused = false;

    isRecording = false;
    mediaRecorder: MediaRecorder | null = null;
    chunks: Blob[] = [];
    statusText = 'Listen to the master, then try yourself.';

    constructor(private zone: NgZone) { }

    async toggleRecording() {
        if (this.isRecording) {
            this.stopRecording();
        } else {
            await this.startRecording();
        }
    }

    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(stream);
            this.chunks = [];

            this.mediaRecorder.ondataavailable = (e) => {
                this.zone.run(() => {
                    this.chunks.push(e.data);
                });
            };

            this.mediaRecorder.onstop = () => {
                this.zone.run(() => {
                    const blob = new Blob(this.chunks, { type: 'audio/wav' });
                    this.audioRecorded.emit(blob);
                    this.statusText = 'Recording finished. Processing...';

                    // Stop all tracks
                    stream.getTracks().forEach(track => track.stop());
                });
            };

            this.mediaRecorder.start();
            this.isRecording = true;
            this.recordingStateChanged.emit(true);
            this.statusText = 'Listening... Read the text above.';
        } catch (err) {
            console.error('Error accessing microphone:', err);
            this.statusText = 'Could not access microphone.';
        }
    }

    onListenToggle() {
        if (!this.isPlaying) {
            this.listenRequested.emit();
        } else if (this.isPaused) {
            this.resumeRequested.emit();
        } else {
            this.pauseRequested.emit();
        }
    }

    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
            this.recordingStateChanged.emit(false);
        }
    }
}
