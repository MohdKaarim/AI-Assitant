import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

interface Surah {
    number: number;
    name_arabic: string;
    name_english: string;
    verses_count: number;
}

@Component({
    selector: 'app-surah-list',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './surah-list.component.html',
    styleUrl: './surah-list.component.css'
})
export class SurahListComponent implements OnInit {
    @Output() surahSelected = new EventEmitter<number>();

    surahs: Surah[] = [];
    selectedSurah: Surah | null = null;
    private apiUrl = 'http://localhost:8000/api';

    constructor(private http: HttpClient) { }

    ngOnInit() {
        this.loadSurahs();
    }

    loadSurahs() {
        this.http.get<{ surahs: Surah[] }>(`${this.apiUrl}/surahs`).subscribe({
            next: (response) => {
                this.surahs = response.surahs;
            },
            error: (err) => {
                console.error('Error loading surahs:', err);
            }
        });
    }

    selectSurah(surah: Surah) {
        this.selectedSurah = surah;
        this.surahSelected.emit(surah.number);
    }
}
