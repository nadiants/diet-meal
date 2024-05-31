// Scenario : From open App to Home Screen App Diet Meal

describe('Open Diet Meal Application', function() {
    it('should open Diet Meal app', async () => {
        const welcome = await $('//android.widget.TextView[@resource-id="com.fghilmany.dietmealapp:id/header_welcome"]');
        
        // assert test Welcome... di halaman welcome page
        await expect(welcome).toHaveAttrContaining('text', 'Welcome...');
    })

    it('input data in welcome page', async () => {
        await $('//android.widget.EditText[@resource-id="com.fghilmany.dietmealapp:id/et_name"]').setValue('nadia');
        
        // input weight
        await $('//android.widget.EditText[@resource-id="com.fghilmany.dietmealapp:id/et_weight"]').setValue('44');

        // input height
        await $('//android.widget.EditText[@resource-id="com.fghilmany.dietmealapp:id/et_height"]').setValue('147');
        
        // choose female
        await $('//android.widget.RadioButton[@resource-id="com.fghilmany.dietmealapp:id/rb_female"]').click();

        const buttonNext = await $('//android.widget.Button[@resource-id="com.fghilmany.dietmealapp:id/bt_next"]');
        await driver.hideKeyboard()
        await buttonNext.click();
    })

    it('should open choose daily activities page', async () => {
        const dailyActivities = await $('//android.widget.TextView[@resource-id="com.fghilmany.dietmealapp:id/title_activity"]');
        
        // assert test Aktivitas sehari-hari di halaman choose daily activities page
        await expect(dailyActivities).toHaveAttrContaining('text', 'Aktivitas sehari-hari');
    })

    it('choose daily activities', async () => {
        // choose sekolah, kuliah, kerja kantor, dsj.
        await $('//android.widget.RadioButton[@resource-id="com.fghilmany.dietmealapp:id/rb_low_to_medium"]').click();
        
        // click button selesai
        await $('//android.widget.Button[@resource-id="com.fghilmany.dietmealapp:id/bt_finish"]').click();     
    })

    it('should open home page', async () => {
        const home = await $('//android.widget.FrameLayout[@content-desc="Home"]');
        
        // assert selected true di halaman home page
        await expect(home).toHaveAttrContaining('selected', true);
    })
})