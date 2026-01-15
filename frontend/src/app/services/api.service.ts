
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface OCRResponse {
    extracted_text: string;
    language: string;
}

export interface AnalysisResponse {
    spoken_text: string;
    reference_text: string;
    match_score: number;
    ipa_transcription?: {
        expected: string;
        spoken: string;
    };
    tajweed_errors?: Array<{
        code: string;
        title: string;
        description: string;
        severity: string;
        word_index?: number;
        error_type?: string;
    }>;
}

@Injectable({
    providedIn: 'root'
})
export class ApiService {
    private apiUrl = 'http://localhost:8000/api';

    constructor(private http: HttpClient) { }

    uploadImage(file: File, lang: string = 'eng'): Observable<OCRResponse> {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('lang', lang);
        return this.http.post<OCRResponse>(`${this.apiUrl}/ocr`, formData);
    }

    analyzeAudio(audioBlob: Blob, referenceText: string): Observable<AnalysisResponse> {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.wav');
        formData.append('reference_text', referenceText);
        return this.http.post<AnalysisResponse>(`${this.apiUrl}/analyze`, formData);
    }

    translateText(text: string): Observable<{ original: string, translation: string, transliteration: string }> {
        const formData = new FormData();
        formData.append('text', text);
        return this.http.post<{ original: string, translation: string, transliteration: string }>(`${this.apiUrl}/translate`, formData);
    }
}
