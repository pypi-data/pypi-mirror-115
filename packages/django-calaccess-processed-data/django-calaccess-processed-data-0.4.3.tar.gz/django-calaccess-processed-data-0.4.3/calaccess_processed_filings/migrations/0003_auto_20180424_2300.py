# Generated by Django 2.0.4 on 2018-04-24 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calaccess_processed_filings', '0002_auto_20180424_2226'),
    ]

    operations = [
        migrations.CreateModel(
            name='Form496Part2Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_item', models.IntegerField(db_index=True, help_text='Line number of the filing form where the transaction is itemized (from S496_CD.LINE_ITEM)', verbose_name='line item')),
                ('expense_date', models.DateField(help_text='Date or expense (from S496_CD.EXP_DATE)', null=True, verbose_name='expense date')),
                ('amount', models.DecimalField(decimal_places=2, help_text='Amount paid to the payee in the period covered by the filing (from S496_CD.AMOUNT)', max_digits=14, verbose_name='amount')),
                ('transaction_id', models.CharField(db_index=True, help_text='Identifies a unique transaction across versions of the a given Schedule 496 filing (from S496_CD.TRAN_ID)', max_length=20, verbose_name='transaction id')),
                ('payment_description', models.CharField(blank=True, help_text='Purpose of payment and/or description/explanation (from S496_CD.EXPN_DSCR)', max_length=400, verbose_name='payment description')),
                ('memo_code', models.CharField(blank=True, help_text='A description offered by the filer', max_length=500, verbose_name='memo code')),
                ('memo_reference_number', models.CharField(blank=True, help_text='Reference number for the memo attached to the transaction (from S496_CD.MEMO_REFNO)', max_length=20, verbose_name='memo reference number')),
                ('filing', models.ForeignKey(db_constraint=False, help_text='Unique identification number for the Schedule 496 filing (from S496_CD.FILING_ID)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='independent_expenditures_made', to='calaccess_processed_filings.Form496Filing')),
            ],
            options={
                'verbose_name': 'Form 496 (Late Independent Expenditure) Part 2 item',
            },
        ),
        migrations.CreateModel(
            name='Form496Part2ItemVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_item', models.IntegerField(db_index=True, help_text='Line number of the filing form where the transaction is itemized (from S496_CD.LINE_ITEM)', verbose_name='line item')),
                ('expense_date', models.DateField(help_text='Date or expense (from S496_CD.EXP_DATE)', null=True, verbose_name='expense date')),
                ('amount', models.DecimalField(decimal_places=2, help_text='Amount paid to the payee in the period covered by the filing (from S496_CD.AMOUNT)', max_digits=14, verbose_name='amount')),
                ('transaction_id', models.CharField(db_index=True, help_text='Identifies a unique transaction across versions of the a given Schedule 496 filing (from S496_CD.TRAN_ID)', max_length=20, verbose_name='transaction id')),
                ('payment_description', models.CharField(blank=True, help_text='Purpose of payment and/or description/explanation (from S496_CD.EXPN_DSCR)', max_length=400, verbose_name='payment description')),
                ('memo_code', models.CharField(blank=True, help_text='A description offered by the filer', max_length=500, verbose_name='memo code')),
                ('memo_reference_number', models.CharField(blank=True, help_text='Reference number for the memo attached to the transaction (from S496_CD.MEMO_REFNO)', max_length=20, verbose_name='memo reference number')),
                ('filing_version', models.ForeignKey(help_text='Foreign key referring to the version of the Schedule 496 that includes the given expenditure', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='independent_expenditures_made', to='calaccess_processed_filings.Form496FilingVersion')),
            ],
            options={
                'verbose_name': 'Form 496 (Late Independent Expenditure) Part 2 item version',
            },
        ),
        migrations.AlterUniqueTogether(
            name='form496part2itemversion',
            unique_together={('filing_version', 'line_item')},
        ),
        migrations.AlterIndexTogether(
            name='form496part2itemversion',
            index_together={('filing_version', 'line_item')},
        ),
        migrations.AlterUniqueTogether(
            name='form496part2item',
            unique_together={('filing', 'line_item')},
        ),
    ]
