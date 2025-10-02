from flask import render_template, request, redirect, url_for, flash, jsonify, send_file, make_response
from . import results_bp
from models import Vote, Candidate, Party, Voter, db
from sqlalchemy import func
import pandas as pd
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT

@results_bp.route('/live')
def live():
    """Live results page"""
    results = db.session.query(
        Candidate.name.label('candidate_name'),
        Party.name.label('party_name'),
        func.count(Vote.id).label('vote_count')
    ).select_from(Vote).join(
        Candidate, Vote.candidate_id == Candidate.id
    ).join(
        Party, Candidate.party_id == Party.id
    ).group_by(
        Candidate.id, Candidate.name, Party.name
    ).order_by(
        func.count(Vote.id).desc()
    ).all()
    
    nota_votes = Vote.query.filter_by(candidate_id=None).count()
    total_votes = Vote.query.count()
    total_voters = Voter.query.count()
    turnout_percentage = (total_votes / total_voters * 100) if total_voters > 0 else 0
    
    return render_template('results/live.html', 
                         results=results,
                         nota_votes=nota_votes,
                         total_votes=total_votes,
                         total_voters=total_voters,
                         turnout_percentage=turnout_percentage,
                         now=datetime.now().strftime('%B %d, %Y at %I:%M %p'))

@results_bp.route('/export/csv')
def export_csv():
    """Export results as CSV"""
    results = db.session.query(
        Candidate.name.label('Candidate'),
        Party.name.label('Party'),
        func.count(Vote.id).label('Votes')
    ).select_from(Vote).join(
        Candidate, Vote.candidate_id == Candidate.id
    ).join(
        Party, Candidate.party_id == Party.id
    ).group_by(
        Candidate.id, Candidate.name, Party.name
    ).order_by(
        func.count(Vote.id).desc()
    ).all()
    
    df = pd.DataFrame(results, columns=['Candidate', 'Party', 'Votes'])
    
    nota_votes = Vote.query.filter_by(candidate_id=None).count()
    if nota_votes > 0:
        df = pd.concat([df, pd.DataFrame([['NOTA', '-', nota_votes]], columns=['Candidate', 'Party', 'Votes'])], ignore_index=True)
    
    df.loc['Total'] = ['', 'Total Votes', df['Votes'].sum()]
    
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return send_file(output, 
                    mimetype='text/csv',
                    as_attachment=True,
                    download_name=f'election_results_{timestamp}.csv')

@results_bp.route('/export/excel')
def export_excel():
    """Export results as Excel"""
    results = db.session.query(
        Candidate.name.label('Candidate'),
        Party.name.label('Party'),
        func.count(Vote.id).label('Votes')
    ).select_from(Vote).join(
        Candidate, Vote.candidate_id == Candidate.id
    ).join(
        Party, Candidate.party_id == Party.id
    ).group_by(
        Candidate.id, Candidate.name, Party.name
    ).order_by(
        func.count(Vote.id).desc()
    ).all()
    
    df = pd.DataFrame(results, columns=['Candidate', 'Party', 'Votes'])
    
    nota_votes = Vote.query.filter_by(candidate_id=None).count()
    if nota_votes > 0:
        df = pd.concat([df, pd.DataFrame([['NOTA', '-', nota_votes]], columns=['Candidate', 'Party', 'Votes'])], ignore_index=True)
    
    df.loc['Total'] = ['', 'Total Votes', df['Votes'].sum()]
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Election Results', index=False)
    output.seek(0)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return send_file(output, 
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    as_attachment=True,
                    download_name=f'election_results_{timestamp}.xlsx')

@results_bp.route('/export/pdf')
def export_pdf():
    """Export results as PDF"""
    results = db.session.query(
        Candidate.name.label('candidate_name'),
        Party.name.label('party_name'),
        func.count(Vote.id).label('vote_count')
    ).select_from(Vote).join(
        Candidate, Vote.candidate_id == Candidate.id
    ).join(
        Party, Candidate.party_id == Party.id
    ).group_by(
        Candidate.id, Candidate.name, Party.name
    ).order_by(
        func.count(Vote.id).desc()
    ).all()
    
    nota_votes = Vote.query.filter_by(candidate_id=None).count()
    total_votes = Vote.query.count()
    
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    title = Paragraph("Election Results Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    timestamp = datetime.now().strftime('%B %d, %Y at %I:%M %p')
    date_text = Paragraph(f"<para align=center>Generated on {timestamp}</para>", styles['Normal'])
    elements.append(date_text)
    elements.append(Spacer(1, 0.3*inch))
    
    data = [['Rank', 'Candidate', 'Party', 'Votes', 'Percentage']]
    
    for idx, result in enumerate(results, 1):
        percentage = (result.vote_count / total_votes * 100) if total_votes > 0 else 0
        data.append([
            str(idx),
            result.candidate_name,
            result.party_name,
            str(result.vote_count),
            f"{percentage:.2f}%"
        ])
    
    if nota_votes > 0:
        nota_percentage = (nota_votes / total_votes * 100) if total_votes > 0 else 0
        data.append([
            '-',
            'NOTA',
            '-',
            str(nota_votes),
            f"{nota_percentage:.2f}%"
        ])
    
    data.append(['', '', 'Total', str(total_votes), '100.00%'])
    
    table = Table(data, colWidths=[0.8*inch, 2.5*inch, 2*inch, 1*inch, 1.2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8e8e8')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f5f5f5')])
    ]))
    
    elements.append(table)
    
    doc.build(elements)
    output.seek(0)
    
    timestamp_file = datetime.now().strftime('%Y%m%d_%H%M%S')
    return send_file(output, 
                    mimetype='application/pdf',
                    as_attachment=True,
                    download_name=f'election_results_{timestamp_file}.pdf')