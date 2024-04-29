import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StatCampingComponent } from './stat-camping.component';

describe('StatCampingComponent', () => {
  let component: StatCampingComponent;
  let fixture: ComponentFixture<StatCampingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StatCampingComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(StatCampingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
