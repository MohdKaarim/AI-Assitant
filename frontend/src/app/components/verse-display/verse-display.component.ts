import { Component, Input, OnChanges, SimpleChanges, ChangeDetectorRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { AudioRecorderComponent } from '../audio-recorder/audio-recorder.component';
import { ApiService } from '../../services/api.service';
import { convertWebMToWav } from '../../utils/audio-converter';
import { AudioPlayer } from '../../utils/audio-player';

interface VerseWord {
    arabic: string;
    english: string;
}

interface Verse {
    number: number;
    text_arabic: string;
    text_english: string;
    text_transliteration?: string;
    audio_url?: string;
    words?: VerseWord[];
}

interface SurahData {
    number: number;
    name_arabic: string;
    name_english: string;
    verses_count: number;
    verses: Verse[];
}

@Component({
    selector: 'app-verse-display',
    standalone: true,
    imports: [CommonModule, AudioRecorderComponent],
    templateUrl: './verse-display.component.html',
    styleUrl: './verse-display.component.css'
})
export class VerseDisplayComponent implements OnChanges {
    @ViewChild(AudioRecorderComponent) recorder!: AudioRecorderComponent;
    @Input() surahNumber!: number;

    surahData: SurahData | null = null;
    currentVerseIndex = 0;
    currentVerse: Verse | null = null;
    displayWords: VerseWord[] = [];
    activeWordIndex: number | null = null;
    wordAccuracies: (number | null)[] = [];
    mistakes: any[] = [];
    isAnalyzing = false;
    isRecording = false;

    // Real-time feedback
    matchScore: number | null = null;
    spokenText: string = '';
    showFeedback = false;
    autoAdvanceTimer: any = null;
    isPlayingReference = false;
    isPaused = false;
    karaokeTimer: any = null;

    private readonly apiUrl = 'http://localhost:8000/api';

    constructor(
        private http: HttpClient,
        private api: ApiService,
        private cdr: ChangeDetectorRef
    ) { }

    ngOnChanges(changes: SimpleChanges) {
        if (changes['surahNumber'] && this.surahNumber) {
            this.loadSurah();
        }
    }

    loadSurah() {
        this.http.get<SurahData>(`${this.apiUrl}/surah/${this.surahNumber}`).subscribe({
            next: (data) => {
                this.surahData = data;
                this.currentVerseIndex = 0;
                this.updateCurrentVerse();
                this.cdr.detectChanges();
            },
            error: (err) => {
                console.error('Error loading surah:', err);
            }
        });
    }

    previousVerse() {
        if (this.currentVerseIndex > 0) {
            this.currentVerseIndex--;
            this.updateCurrentVerse();
        }
    }

    nextVerse() {
        if (this.surahData && this.currentVerseIndex < this.surahData.verses.length - 1) {
            this.currentVerseIndex++;
            this.updateCurrentVerse();
        }
    }

    updateCurrentVerse() {
        if (this.surahData) {
            this.currentVerse = this.surahData.verses[this.currentVerseIndex];

            if (this.currentVerse.words && this.currentVerse.words.length > 0) {
                this.displayWords = this.currentVerse.words;
            } else {
                // Fallback to splitting by space if no word-level data exists
                this.displayWords = this.currentVerse.text_arabic.split(/\s+/).map(w => ({
                    arabic: w,
                    english: ''
                }));
            }

            this.wordAccuracies = new Array(this.displayWords.length).fill(null);
            this.activeWordIndex = null;
            this.mistakes = [];
            this.matchScore = null;
            this.spokenText = '';
            this.showFeedback = false;

            // Clear any pending auto-advance
            if (this.autoAdvanceTimer) {
                clearTimeout(this.autoAdvanceTimer);
                this.autoAdvanceTimer = null;
            }

            // Auto-play reference audio
            setTimeout(() => this.playReference(), 500);
        }
    }

    advanceToNextVerse() {
        if (this.surahData && this.currentVerseIndex < this.surahData.verses.length - 1) {
            this.nextVerse();
        }
    }

    async playReference() {
        if (!this.currentVerse?.audio_url || this.isPlayingReference) return;

        this.isPlayingReference = true;
        this.isPaused = false;
        this.activeWordIndex = null;
        this.wordAccuracies = new Array(this.displayWords.length).fill(null);

        this.startKaraoke();

        try {
            await AudioPlayer.playUrl(this.currentVerse.audio_url);
            this.stopKaraoke();

            // Automatically start recording after reference audio ends
            if (this.recorder && !this.isAnalyzing) {
                setTimeout(() => {
                    this.onRecordingStateChanged(true);
                    this.recorder.startRecording();
                    this.cdr.detectChanges();
                }, 300); // 300ms pause for better UX
            }
        } catch (err) {
            console.error('Error playing reference audio:', err);
            this.stopKaraoke();
        } finally {
            this.isPlayingReference = false;
            this.isPaused = false;
            this.cdr.detectChanges();
        }
    }

    pauseReference() {
        AudioPlayer.pause();
        this.isPaused = true;
        this.pauseKaraoke();
        this.cdr.detectChanges();
    }

    resumeReference() {
        AudioPlayer.resume();
        this.isPaused = false;
        this.resumeKaraoke();
        this.cdr.detectChanges();
    }

    private startKaraoke() {
        this.stopKaraoke();
        const wordInterval = 600;

        this.karaokeTimer = setInterval(() => {
            if (this.isPaused) return;

            if (this.activeWordIndex === null) this.activeWordIndex = 0;
            else if (this.activeWordIndex < this.displayWords.length - 1) {
                this.activeWordIndex++;
            } else {
                this.stopKaraoke();
            }
            this.cdr.detectChanges();
        }, wordInterval);
    }

    private pauseKaraoke() {
        // Just let the interval skip its work via isPaused check
    }

    private resumeKaraoke() {
        // Just let the interval resume its work
    }

    private stopKaraoke() {
        if (this.karaokeTimer) {
            clearInterval(this.karaokeTimer);
            this.karaokeTimer = null;
        }
        this.activeWordIndex = null;
    }

    onRecordingStateChanged(isRecording: boolean) {
        this.isRecording = isRecording;
        if (isRecording) {
            // Start karaoke guide for recording
            this.startKaraoke();
        } else {
            this.stopKaraoke();
        }
    }

    async onAudioRecorded(audioBlob: Blob) {
        if (!this.currentVerse) return;

        this.isRecording = false; // Reset recording state when audio is received
        this.isAnalyzing = true;
        this.mistakes = [];

        try {
            const wavBlob = await convertWebMToWav(audioBlob);
            const analysisText = this.displayWords.map(w => w.arabic).join(' ');

            this.api.analyzeAudio(wavBlob, analysisText).subscribe({
                next: (res: any) => {
                    this.isAnalyzing = false;
                    this.wordAccuracies = res.word_accuracies || [];

                    // Display real-time feedback
                    this.matchScore = Math.round((res.match_score || 0) * 100);
                    this.spokenText = res.spoken_text || '';
                    this.showFeedback = true;

                    // Handle Tajweed errors if present
                    if (res.tajweed_errors && res.tajweed_errors.length > 0) {
                        this.mistakes = res.tajweed_errors;
                    }

                    // Auto-advance to next verse after 3 seconds if score is good
                    if (this.matchScore >= 70) {
                        this.autoAdvanceTimer = setTimeout(() => {
                            this.advanceToNextVerse();
                            this.cdr.detectChanges();
                        }, 3000);
                    }

                    this.cdr.detectChanges();
                },
                error: (err) => {
                    console.error(err);
                    this.isAnalyzing = false;
                    this.cdr.detectChanges();
                }
            });
        } catch (e) {
            console.error("Audio conversion failed", e);
            this.isAnalyzing = false;
        }
    }

    getTajweedMessage(errorType: string): string {
        const messages: any = {
            'qalqalah_missing': 'Make sure to bounce on the letters (ق ط ب ج د) when they have a Sukun.',
            'ghunna_incorrect': 'Ensure proper nasalization timing (2 counts) on Noon and Mim Mushaddadah.',
            'madd_short': 'You shortened a long vowel. Stretch the sound for the correct duration.',
            'heavy_letter_light': 'This letter requires raising the back of the tongue (Tafkheem).'
        };
        return messages[errorType] || 'Please review this pronunciation.';
    }
}
