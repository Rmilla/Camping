import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StatGeneralComponent } from './stat-general.component';

describe('StatGeneralComponent', () => {
  let component: StatGeneralComponent;
  let fixture: ComponentFixture<StatGeneralComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StatGeneralComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(StatGeneralComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
