from django.db import migrations, models


def merge_datalocation_into_reductionrun(apps, _):
    """
    Moves the values from the DataLocation model into the field of the ReductionRun
    """
    ReductionRun = apps.get_model("reduction_viewer", "ReductionRun")
    for run in ReductionRun.objects.all():
        run.data_location_tmp = run.data_location.first().file_path


class Migration(migrations.Migration):

    dependencies = [
        ('reduction_viewer', '0006_reductionrun_reduction_host'),
    ]

    operations = [
        # Add a data_location_tmp field, suffixed with _tmp to avoid clash with the
        # model's foreign key field run.data_location
        migrations.AddField(
            model_name='reductionrun',
            name='data_location_tmp',
            field=models.CharField(default='none', max_length=255),
            preserve_default=False,
        ),
        # copy the data_location_tmp field into the run.data_location field
        migrations.RunPython(merge_datalocation_into_reductionrun),
        # deletes the DataLocation model and the data in it
        migrations.DeleteModel(name='DataLocation', ),
        # renames the data_location_tmp we made to just be data_location
        migrations.RenameField(model_name='reductionrun', old_name='data_location_tmp', new_name='data_location'),
    ]
