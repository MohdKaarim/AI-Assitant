import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { SurahListComponent } from '../surah-list/surah-list.component';
import { VerseDisplayComponent } from '../verse-display/verse-display.component';

@Component({
    selector: 'app-tutor-interface',
    standalone: true,
    imports: [CommonModule, RouterLink, SurahListComponent, VerseDisplayComponent],
    templateUrl: './tutor-interface.component.html',
    styleUrl: './tutor-interface.component.css'
})
export class TutorInterfaceComponent {
    selectedSurahNumber: number | null = null;

    onSurahSelected(surahNumber: number) {
        this.selectedSurahNumber = surahNumber;
    }

    backToSurahList() {
        this.selectedSurahNumber = null;
    }

    nextSurah() {
        if (this.selectedSurahNumber) {
            // Circular navigation: 1-114
            this.selectedSurahNumber = (this.selectedSurahNumber % 114) + 1;
        }
    }
}
